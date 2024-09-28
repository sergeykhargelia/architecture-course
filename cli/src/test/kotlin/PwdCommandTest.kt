import org.junit.jupiter.api.Assertions.*

class PwdCommandTest {
    @org.junit.jupiter.api.Test
    fun `pwd test`() {
        val outputBuffer = StringBuilder()
        val command = PwdCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf()
        )
        command.execute()
        assert(outputBuffer.toString().endsWith("cli"))
    }
}