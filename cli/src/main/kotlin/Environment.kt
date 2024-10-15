class Environment : EnvironmentReader, EnvironmentWriter {
    private val variables: MutableMap<String, String> = mutableMapOf()

    override fun getVariable(variable: String): String {
        return variables[variable] ?: ""
    }

    override fun setVariable(variable: String, value: String) {
        variables[variable] = value
    }
}
