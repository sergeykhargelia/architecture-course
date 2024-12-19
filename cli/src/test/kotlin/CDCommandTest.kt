import kotlin.test.assertEquals
import kotlin.test.assertNotEquals

class CDCommandTest {

    @org.junit.jupiter.api.Test
    fun `cd home test`() {
        val outputBuffer = StringBuilder()
        val environment = Environment()
        val oldDirectory = environment.currentDirectory
        val command = CDCommand(
            environment,
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf()
        )
        val code = command.execute().returnCode
        assertEquals(0, code)
        assertNotEquals(oldDirectory, environment.currentDirectory)
    }

    @org.junit.jupiter.api.Test
    fun `cd testdir test`() {
        val outputBuffer = StringBuilder()
        val environment = Environment()
        val testDir = "src/test/resources/testdir"
        val command = CDCommand(
            environment,
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(testDir)
        )
        val code = command.execute().returnCode
        assertEquals(0, code)
        assert(environment.currentDirectory.endsWith(testDir))
    }
}
