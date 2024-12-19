import java.nio.file.Path
import java.nio.file.Paths

interface IEnvironment : EnvironmentReader, EnvironmentWriter, EnvironmentDirectory

class Environment : IEnvironment {
    private val variables: MutableMap<String, String> = mutableMapOf()
    override var currentDirectory: Path = Paths.get("").toAbsolutePath()

    override fun getVariable(variable: String): String {
        return variables[variable] ?: ""
    }

    override fun setVariable(variable: String, value: String) {
        variables[variable] = value
    }
}

class MockEnvironment: IEnvironment {
    override fun getVariable(variable: String): String {
        TODO("Not yet implemented")
    }

    override fun setVariable(variable: String, value: String) {
        TODO("Not yet implemented")
    }

    override var currentDirectory: Path
        get() = TODO("Not yet implemented")
        set(value) {}

}