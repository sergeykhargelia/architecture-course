import org.junit.jupiter.api.Assertions.*

class CommandExecutorTest {
    private val env = MockEnvironment()
    private val executor = CommandExecutor()

    @org.junit.jupiter.api.Test
    fun executeBasic() {
        val middleBuffer = Buffer()
        val outputBuffer = Buffer()
        val executionResult = executor.executeCommands(listOf(
            EchoCommand(env, MockIStream(), middleBuffer, MockOStream(), listOf("testdir")),
            CatCommand(env, middleBuffer, outputBuffer, MockOStream(), emptyList())
        ))

        assertEquals(false, executionResult.terminate)
        assertEquals(0, executionResult.returnCode)
        assertEquals("testdir", outputBuffer.readLine())
    }

    @org.junit.jupiter.api.Test
    fun `execute sequence of commands with exit`() {
        val executionResult = executor.executeCommands(listOf(
            ExitCommand(env, MockIStream(), MockOStream(), MockOStream(), listOf()),
            ExternalCommand(env, MockIStream(), MockOStream(), MockOStream(), listOf("abcdef"))
        ))

        assertEquals(true, executionResult.terminate)
        assertEquals(0, executionResult.returnCode)
    }

    @org.junit.jupiter.api.Test
    fun `non zero exit code`() {
        val executionResult = executor.executeCommands(listOf(
            ExternalCommand(Environment(), MockIStream(), MockOStream(), MockOStream(), listOf("abcdef"))
        ))

        assertEquals(false, executionResult.terminate)
        assertNotEquals(0, executionResult.returnCode)
    }
}