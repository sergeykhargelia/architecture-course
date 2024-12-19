class PWDCommandTest {
    @org.junit.jupiter.api.Test
    fun `pwd test`() {
        val outputBuffer = StringBuilder()
        val environment = Environment()
        val command = PWDCommand(
            environment,
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf()
        )
        command.execute()
        assert(outputBuffer.toString().endsWith("cli"))
    }
}