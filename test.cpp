#include <string_view>
#include <cctype>
#include <stdexcept>
#include <set>
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <vector>
#include <map>
#include <sstream>
#include <iostream>

namespace cpp_syntax_highlighter {

enum class token_type {
    none,
    integer_literal,
    floating_point_literal,
    string_literal,
    char_literal,
    operator_,
    identifier,
    comment
};

enum class scan_state {
    start,
    white,
    begin_number,
    period_begin,
    float_,
    str_ongoing,
    str_escape,
    str_end,
    char_ongoing,
    char_escape,
    char_end,
    comment_or_division,
    comment,
    operator_,
    identifier,
    invalid_start
};

std::set<std::string> operators = {
    "+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">=", "||", "&&", "++", "--", "::", "&", "(", ")", "[", "]", "{", "}", ";", ".", ",", "#include", "?", ":", "!"
};

token_type scan(const std::string &line, std::string_view::size_type &pos) {
    std::string cur_op; // memory for operator parsing
    scan_state state = scan_state::start;

    while (pos <= line.size()) {
        // Append space at the end to handle end of line in-loop.
        char c = pos == line.size() ? ' ' : line[pos];

        switch (state) {
        case scan_state::start:
            if (c == ' ' || c == '\t') {
                state = scan_state::white;
            } else if (std::isdigit(c)) {
                state = scan_state::begin_number;
            } else if (c == '.') {
                state = scan_state::period_begin;
            } else if (c == '"') {
                state = scan_state::str_ongoing;
            } else if (c == '\'') {
                state = scan_state::char_ongoing;
            } else if (c == '/') {
                state = scan_state::comment_or_division;
            } else if (std::find_if(operators.begin(), operators.end(), [c](const std::string &op) { return op[0] == c; }) != operators.end()) {
                state = scan_state::operator_;
                cur_op = c;
            } else if (std::isalpha(c) || c == '_') {
                state = scan_state::identifier;
            } else {
                state = scan_state::invalid_start;
            }
            break;
        case scan_state::white:
            if (c == ' ' || c == '\t') {
                state = scan_state::white;
            } else {
                return token_type::none;
            }
            break;
        case scan_state::begin_number:
            if (std::isdigit(c)) {
                state = scan_state::begin_number;
            } else if (c == '.') {
                state = scan_state::float_;
            } else {
                return token_type::integer_literal;
            }
            break;
        case scan_state::period_begin:
            if (std::isdigit(c)) {
                state = scan_state::float_;
            } else if (std::isalpha(c) || c == '_') {
                return token_type::operator_;
            } else {
                throw std::invalid_argument("expected digit or identifier");
            }
            break;
        case scan_state::float_:
            if (std::isdigit(c)) {
                state = scan_state::float_;
            } else {
                return token_type::floating_point_literal;
            }
            break;
        case scan_state::str_ongoing:
            if (c == '\\') {
                state = scan_state::str_escape;
            } else if (c == '"') {
                state = scan_state::str_end;
            } else {
                state = scan_state::str_ongoing;
            }
            break;
        case scan_state::str_escape:
            state = scan_state::str_ongoing;
            break;
        case scan_state::str_end:
            return token_type::string_literal;
        case scan_state::char_ongoing:
            if (c == '\\') {
                state = scan_state::char_escape;
            } else if (c == '\'') {
                state = scan_state::char_end;
            } else {
                state = scan_state::char_ongoing;
            }
            break;
        case scan_state::char_escape:
            state = scan_state::char_ongoing;
            break;
        case scan_state::char_end:
            return token_type::char_literal;
        case scan_state::comment_or_division:
            if (c == '/') {
                state = scan_state::comment;
            } else {
                cur_op = '/';
                if (std::find_if(operators.begin(), operators.end(), [=](const std::string &op) { return op.starts_with(cur_op + c); }) != operators.end()) {
                    state = scan_state::operator_;
                    cur_op.push_back(c);
                } else {
                    return token_type::operator_;
                }
            }
            break;
        case scan_state::comment:
            if (pos == line.size()) {
                return token_type::comment;
            } else {
                state = scan_state::comment;
            }
            break;
        case scan_state::operator_:
            if (std::find_if(operators.begin(), operators.end(), [=](const std::string &op) { return op.starts_with(cur_op + c); }) != operators.end()) {
                state = scan_state::operator_;
                cur_op.push_back(c);
            } else if (operators.contains(cur_op)) {
                return token_type::operator_;
            } else {
                throw std::invalid_argument("invalid operator");
            }
            break;
        case scan_state::identifier:
            if (std::isalnum(c) || c == '_') {
                state = scan_state::identifier;
            } else {
                return token_type::identifier;
            }
            break;
        case scan_state::invalid_start:
            throw std::invalid_argument("invalid character");
        default:
            // unreachable
            break;
        }

        // If we are at the last extra space character and no token was ended (due to white character at the end of line),
        // do not advance pos.
        if (pos == line.size()) {
            // Handle invalid states.
            switch (state) {
            case scan_state::period_begin:
                throw std::invalid_argument("expected digit or identifier");
            case scan_state::str_ongoing:
            case scan_state::str_escape:
                throw std::invalid_argument("expected \"");
            case scan_state::char_ongoing:
            case scan_state::char_escape:
                throw std::invalid_argument("expected '");
            default:
                return token_type::none;
            }
        }

        pos++;
    }

    // unreachable
    return token_type::none;
}

} // namespace cpp_syntax_highlighter

using namespace cpp_syntax_highlighter;
namespace fs = std::filesystem;

std::string read_file(const fs::path &path) {
	if (!fs::exists(path))
		throw std::runtime_error("File not found:\n" + path.string());

	std::ifstream stream(path, std::ifstream::in);
	std::string buffer;

	stream.seekg(0, std::ios::end);
	buffer.reserve(stream.tellg());
	stream.seekg(0, std::ios::beg);

	buffer.assign(
			std::istreambuf_iterator<char>(stream),
			std::istreambuf_iterator<char>());
	return buffer;
}

void replace_inplace(std::string &str, std::string_view from, std::string_view to) {
	size_t pos = 0;

	while((pos = str.find(from, pos)) != std::string::npos) {
		str.replace(pos, from.size(), to);
		pos += to.size();
	}
}

std::string replace(std::string str, std::string_view from, std::string_view to) {
    replace_inplace(str, from, to);
    return str;
}

std::map<token_type, std::string> class_names{
    {token_type::integer_literal, "int"},
    {token_type::floating_point_literal, "float"},
    {token_type::string_literal, "str"},
    {token_type::char_literal, "char"},
    {token_type::comment, "comm"},
    {token_type::operator_, "op"},
    {token_type::identifier, "id"}
};

std::set<std::string> keywords{
    "if", "else", "while", "enum", "class", "switch", "break", "return", "case", "default", "for", "do", "continue", "const", "constexpr", "static", "extern", "inline", "namespace", "using", "template", "typename", "typedef", "struct", "union", "public", "private", "protected", "friend", "virtual", "override", "final", "new", "delete", "operator", "this", "nullptr", "true", "false", "void", "int", "float", "double", "char", "bool"
};

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cout << "Usage: [input-source-file] [output_html-file]" << std::endl;
        return 1;
    }

    std::string in_path = argv[1]; // C++ source file
    std::string out_path = argv[2]; // HTML output file

    std::string source = read_file(in_path);
    std::vector<std::string> lines;
    std::string line;
    for (char c : source) {
        if (c == '\n') {
            lines.push_back(line);
            line.clear();
        } else {
            line.push_back(c);
        }
    }

    std::stringstream out;
    out << "<!DOCTYPE html>" << std::endl;
    out << "<html>" << std::endl;
    out << "<head>" << std::endl;
    out << "<title>" << in_path << "</title>" << std::endl;
    out << "<style>" << std::endl;
    out << "body, pre { font-family: monospace; background-color: #223; margin: 0; }" << std::endl;
    out << ".int { color: blue; }" << std::endl;
    out << ".float { color: blue; }" << std::endl;
    out << ".str { color: green; }" << std::endl;
    out << ".char { color: green; }" << std::endl;
    out << ".comm { color: gray; }" << std::endl;
    out << ".op { color: yellow; }" << std::endl;
    out << ".id { color: #DDD; }" << std::endl;
    out << ".kw { color: orange; }" << std::endl;
    out << "</style>" << std::endl;
    out << "</head>" << std::endl;
    out << "<body>" << std::endl;
    out << "<pre>" << std::endl;

    for (size_t line_i = 0; line_i < lines.size(); line_i++) {
        const std::string &line = lines[line_i];
        size_t pos = 0;
        while (pos < line.size()) {
            size_t start_pos = pos;
            token_type token;
            try {
                token = scan(line, pos);
            } catch (std::exception &e) {
                std::cout << "[" << (line_i + 1) << ", " << (pos + 1) << "] ";
                std::cout << e.what() << std::endl;
                std::cout << line << std::endl;
                for (size_t i = 0; i < start_pos; i++) {
                    if (line[i] == '\t') {
                        std::cout << "\t";
                    } else {
                        std::cout << " ";
                    }
                }
                std::cout << std::string(pos - start_pos, '^') << std::endl;
                return 1;
            }
            size_t token_size = pos - start_pos;
            
            switch (token) {
            case token_type::none:
                out << replace(replace(line.substr(start_pos, token_size), "<", "&lt"), ">", "&gt");
                break;
            default:
                std::string class_name = class_names[token];
                if (class_name == "id" && keywords.contains(line.substr(start_pos, token_size))) {
                    class_name = "kw";
                }
                out << "<span class=\"" << class_name << "\">";
                out << replace(replace(line.substr(start_pos, token_size), "<", "&lt"), ">", "&gt");
                out << "</span>";
                break;
            }
        }
        out << std::endl;
    }

    out << "</pre>" << std::endl;
    out << "</body>" << std::endl;
    out << "</html>" << std::endl;

    std::ofstream os(out_path, std::ifstream::out);
    os << out.str();

    return 0;
}

// int main() {
//     while (true) {
//         // std::cout << "Line: ";
//         std::string line;
//         std::getline(std::cin, line);
//         size_t pos = 0;
//         // try {
//             while (pos < line.size()) {
//                 size_t start_pos = pos;
//                 token_type token = scan(line, pos);
//                 size_t token_size = pos - start_pos;
                
//                 switch (token) {
//                 case token_type::none:
//                     break;
//                 default:
//                     std::cout << "<span class=\"" << class_names[token] << "\">";
//                     std::cout << line.substr(start_pos, token_size);
//                     std::cout << "</span>" << std::endl;
//                     break;
//                 }
//             }
//         // }  catch (std::exception &e) {
//         //     std::cout << "[" << (pos + 1) << "] ";
//         //     std::cout << e.what() << std::endl;
//         //     return 1;
//         // }
//     }
//     return 0;
// }
