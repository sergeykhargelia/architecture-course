import java.nio.file.Paths
import kotlin.test.assertEquals

class LSCommandTest {
    @org.junit.jupiter.api.Test
    fun `ls current dir test`() {
        val outputBuffer = StringBuilder()
        val environment = Environment()
        environment.currentDirectory = environment.currentDirectory.resolve(Paths.get("src", "test", "resources", "testdir")).toAbsolutePath()
        val command = LSCommand(
            environment,
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf()
        )
        val code = command.execute().returnCode
        assertEquals(0, code)
        assertEquals("a.txt", outputBuffer.toString())
    }

    @org.junit.jupiter.api.Test
    fun `ls testdir test`() {
        val outputBuffer = StringBuilder()
        val environment = Environment()
        val testDir = "src/test/resources/testdir"
        val command = LSCommand(
            environment,
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(testDir)
        )
        val code = command.execute().returnCode
        assertEquals(0, code)
        assertEquals("a.txt", outputBuffer.toString())
    }
}