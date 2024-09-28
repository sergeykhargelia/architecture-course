import org.junit.jupiter.api.Assertions.*

class CommandSequenceBuilderTest {
    @org.junit.jupiter.api.Test
    fun buildCommands() {
        val env = Environment()
        val builder = CommandSequenceBuilder(env)
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.Cat, listOf("cat", "example.txt")))).first() is CatCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.Echo, listOf("echo", "example.txt")))).first() is EchoCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.WC, listOf("wc", "example.txt")))).first() is WCCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.PWD, listOf("pwd")))).first() is PWDCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.Exit, listOf("exit")))).first() is ExitCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.Assign, listOf("x", "ex")))).first() is AssignCommand
        )
        assertTrue(
            builder.buildCommands(listOf(CommandDescription(CommandType.External, listOf("java", "--version")))).first() is ExternalCommand
        )
    }
}