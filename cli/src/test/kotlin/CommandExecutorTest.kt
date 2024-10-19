import org.junit.jupiter.api.Assertions.*

class CommandExecutorTest {
    private val executor = CommandExecutor()

    @org.junit.jupiter.api.Test
    fun executeBasic() {
        val middleBuffer = Buffer()
        val outputBuffer = Buffer()
        val executionResult = executor.executeCommands(listOf(
            EchoCommand(MockIStream(), middleBuffer, MockOStream(), listOf("a")),
            CatCommand(middleBuffer, outputBuffer, MockOStream(), emptyList())
        ))

        assertEquals(false, executionResult.terminate)
        assertEquals(0, executionResult.returnCode)
        assertEquals("a", outputBuffer.readLine())
    }

    @org.junit.jupiter.api.Test
    fun `execute sequence of commands with exit`() {
        val executionResult = executor.executeCommands(listOf(
            ExitCommand(MockIStream(), MockOStream(), MockOStream(), listOf()),
            ExternalCommand(MockIStream(), MockOStream(), MockOStream(), listOf("abcdef"))
        ))

        assertEquals(true, executionResult.terminate)
        assertEquals(0, executionResult.returnCode)
    }

    @org.junit.jupiter.api.Test
    fun `non zero exit code`() {
        val executionResult = executor.executeCommands(listOf(
            ExternalCommand(MockIStream(), MockOStream(), MockOStream(), listOf("abcdef"))
        ))

        assertEquals(false, executionResult.terminate)
        assertNotEquals(0, executionResult.returnCode)
    }
}