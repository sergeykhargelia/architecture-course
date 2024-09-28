package cli.src.main.kotlin

import Token
import TokenType

class Lexer {
    fun tokenize(input: String): List<Token> {
        val tokens = mutableListOf<Token>()
        var currentQuote: Char? = null
        var tokenType: TokenType? = null
        var data = ""
        for (ch in input) {
            if (ch == '\'' || ch == '"') {
                if (currentQuote == null) {
                    currentQuote = ch
                } else if (ch == currentQuote) {
                    currentQuote = null
                }
                continue
            }
            if (ch == '$' && (currentQuote == null || currentQuote == '"')) {
                if (tokenType != null) {
                    tokens.add(Token(tokenType, data))
                }
                tokenType = TokenType.Variable
                data = ""
                continue
            }
            if (currentQuote == null && (ch == ' ' || ch == '=' /* || ch == '|' */)) {
                if (tokenType != null) {
                    tokens.add(Token(tokenType, data))
                }
                when (ch) {
                    ' ' -> tokens.add(Token(TokenType.Delimiter, " "))
                    '=' -> tokens.add(Token(TokenType.Assign, "="))
                    // TODO: handle pipe
                }
                tokenType = null
                data = ""
                continue
            }
            if (tokenType == null) {
                tokenType = TokenType.Text
            }
            data += ch
        }
        if (tokenType != null) {
            tokens.add(Token(tokenType, data))
        }
        return tokens
    }
}
