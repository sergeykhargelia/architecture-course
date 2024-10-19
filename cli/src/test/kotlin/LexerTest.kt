import org.junit.jupiter.api.Assertions.*

class LexerTest {
    @org.junit.jupiter.api.Test
    fun tokenize() {
        val lexer = Lexer()
        assertEquals(listOf(
            Token(TokenType.Text, "echo"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Variable, "x"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Text, "\$x"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Text, "aaa")
        ), lexer.tokenize("echo \"\$x\" '\$x\' aaa"))

        assertEquals(listOf(
            Token(TokenType.Text, "cat"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Text, "example.txt"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Pipe, "|"),
            Token(TokenType.Delimiter, " "),
            Token(TokenType.Text, "wc")
        ), lexer.tokenize("cat example.txt | wc"))
    }
}