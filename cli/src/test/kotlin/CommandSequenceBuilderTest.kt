import org.junit.jupiter.api.Assertions.*
import kotlin.reflect.KClass

class CommandSequenceBuilderTest {
    private val env = Environment()
    private val builder = CommandSequenceBuilder(env)

    @org.junit.jupiter.api.Test
    fun buildSingleCommand() {
        // (description, expected type, number of arguments to drop)
        val commandsParams: List<Triple<CommandDescription, KClass<*>, Int>> = listOf(
            Triple(CommandDescription(CommandType.Cat, listOf("cat", "example.txt")), CatCommand::class, 1),
            Triple(CommandDescription(CommandType.Echo, listOf("echo", "example.txt")), EchoCommand::class, 1),
            Triple(CommandDescription(CommandType.WC, listOf("wc", "example.txt")), WCCommand::class, 1),
            Triple(CommandDescription(CommandType.PWD, listOf("pwd")), PWDCommand::class, 1),
            Triple(CommandDescription(CommandType.Exit, listOf("exit")), ExitCommand::class, 1),
            Triple(CommandDescription(CommandType.Assign, listOf("x", "kek")), AssignCommand::class, 0),
            Triple(CommandDescription(CommandType.External, listOf("ls", "-lAh")), ExternalCommand::class, 0),
        )

        for ((description, type, argsToDrop) in commandsParams) {
            val result = builder.buildCommands(listOf(description)).first()
            assertTrue(type.isInstance(result))
            assertEquals(description.description.drop(argsToDrop), result.args)
        }
    }

    @org.junit.jupiter.api.Test
    fun buildMultipleCommands() {
        val result = builder.buildCommands(listOf(
            CommandDescription(CommandType.PWD, listOf("pwd")),
            CommandDescription(CommandType.Cat, listOf("cat"))
        ))

        assertTrue(result[0].outputStream == result[1].inputStream)
        assertTrue(result[0] is PWDCommand)
        assertEquals(emptyList<String>(), result[0].args)
        assertTrue(result[1] is CatCommand)
        assertEquals(emptyList<String>(), result[1].args)
    }
}