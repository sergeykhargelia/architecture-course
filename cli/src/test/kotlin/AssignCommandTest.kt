import org.junit.jupiter.api.Assertions.*

class AssignCommandTest {
    @org.junit.jupiter.api.Test
    fun `test assign command`() {
        val env = Environment()
        val command = AssignCommand(
            MockIStream(),
            MockOStream(),
            MockOStream(),
            listOf("variableName", "variableValue"),
            env
        )
        command.execute()
        assertEquals("variableValue", env.getVariable("variableName"))
    }
}