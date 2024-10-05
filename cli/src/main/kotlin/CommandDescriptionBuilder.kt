class CommandDescriptionBuilder {
    private var isAssignCommand: Boolean = false
    private var commandType: CommandType? = null
    private var description = mutableListOf<String>()
    private var string = ""

    fun appendString(data: String) {
        string += data
    }

    fun flush() {
        if (string != "") {
            description.add(string)
            string = ""
        }
    }

    fun setAssignCommandType() {
        isAssignCommand = true
    }

    fun finishCommandDescription() {
        flush()
        if (isAssignCommand) {
            commandType = CommandType.Assign
            return
        }
        if (description.isNotEmpty()) {
            commandType = when (description.first()) {
                "cat" -> CommandType.Cat
                "echo" -> CommandType.Echo
                "wc" -> CommandType.WC
                "pwd" -> CommandType.PWD
                "exit" -> CommandType.Exit
                else -> CommandType.External
            }
        }
    }

    fun getCommand(): CommandDescription? {
        finishCommandDescription()
        val result = commandType?.let { CommandDescription(it, description) }
        isAssignCommand = false
        commandType = null
        description = mutableListOf()
        string = ""
        return result
    }
}
