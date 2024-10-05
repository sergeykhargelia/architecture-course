import org.junit.jupiter.api.Assertions.*

class EchoCommandTest {
    @org.junit.jupiter.api.Test
    fun `test echo command with list of arguments`() {
        val outputBuffer = StringBuilder()
        val arguments = listOf("stay", "out", "of", "my", "territory")
        val command = EchoCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            arguments
        )
        command.execute()
        assertEquals("stay out of my territory", outputBuffer.toString())
    }
}