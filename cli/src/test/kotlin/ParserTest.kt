import org.junit.jupiter.api.Assertions.*

class ParserTest {
    @org.junit.jupiter.api.Test
    fun parseCommands() {
        val env = Environment()
        val parser = Parser(env)
        assertEquals(
            listOf(CommandDescription(CommandType.Cat, listOf("cat", "example.txt"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "cat"), Token(TokenType.Delimiter, " "), Token(TokenType.Text, "example.txt")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.Echo, listOf("echo", "example.txt"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "echo"), Token(TokenType.Delimiter, " "), Token(TokenType.Text, "example.txt")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.WC, listOf("wc", "example.txt"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "wc"), Token(TokenType.Delimiter, " "), Token(TokenType.Text, "example.txt")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.PWD, listOf("pwd"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "pwd")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.Exit, listOf("exit"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "exit")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.Assign, listOf("x", "ex"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "x"), Token(TokenType.Assign, "="), Token(TokenType.Text, "ex")))
        )
        assertEquals(
            listOf(CommandDescription(CommandType.External, listOf("java", "--version"))),
            parser.parseCommands(listOf(Token(TokenType.Text, "java"), Token(TokenType.Delimiter, " "), Token(TokenType.Text, "--version")))
        )
    }
}