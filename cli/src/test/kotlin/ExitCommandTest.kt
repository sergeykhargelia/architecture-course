import org.junit.jupiter.api.Assertions.*

class ExitCommandTest {
    @org.junit.jupiter.api.Test
    fun `test exit command`() {
        val command = ExitCommand(
            MockEnvironment(),
            MockIStream(),
            MockOStream(),
            MockOStream(),
            listOf()
        )
        val executionResult = command.execute()
        assertEquals(0, executionResult.returnCode)
    }
}