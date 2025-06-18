import os, json, asyncio
from openai import OpenAI
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

load_dotenv()
llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# The globally accessible list of tools/resources that the MCP client finds on the server.
functions = []
function_uris = []
messages = []

async def llm_driven_mcp():
	"""An OpenAI LLM chooses which resource(s), defined on
	the MCP server and surfaced to the AI via the MCP client,
	to use for a task"""

		# First, connect an MCP client to the server's I/O using STDIO (server.py is launched as a subprocess).
		# Why 'async with'?
		# 'async is used used because starting and stopping the client/transport is an async operation
		# (client-server handshake is async as per MCP).
		# 'with' is used because the Client object implements a Context Manager. It simplifies allocating
		# and releasing resources for graceful cleanup even during errors, including closing pipes to the server,
		# which is easier than manually writing a 'try...finally' block.
	async with Client(PythonStdioTransport("server.py")) as client:

		# The MCP client fetches all available resources from the MCP server and organizes them.
		await update_tools(client)
		
		# The user asks the LLM a question and the LLM uses the tools it has available, if applicable
		while True:
			prompt:str = input("Enter your financial question (or type 'exit'): ")
			if prompt.lower() == "exit":
				break

			try:
				# Ask the LLM to pick an MCP resource based on the prompt
				messages.append({"role": "user", "content": prompt})
				response = llm_client.chat.completions.create(
					model="gpt-4.1-mini",
					messages=messages,
					tools=functions,
					tool_choice="auto"
				)

				# Parsing the response for tool calls the LLM is requesting, we get a ChatCompletionMessage object that looks like this:
				# ChatCompletionMessage(..., tool_calls=[ChatCompletionMessageToolCall(id='call_AyL1WHEmf6Z1H5BfjG47sEbh', function=Function(arguments='{"ticker":"MSFT"}', name='getEarningsYield'), type='function')])
				# We extract the function name that the LLM wants to call and the arguments (the stock ticker)
				# TO DO: Put this all in a try-catch section, in case the LLM decided not to use a tool
				tool_call = response.choices[0].message.tool_calls[0]
				function_name = tool_call.function.name
				arguments = json.loads(tool_call.function.arguments)


				# Call the MCP resource by name
				# function_id = getattr(client, function_name)
				# call_resource = await function_id(**arguments)
				index = 0
				for f in functions:
					if f.get("function").get("name") == function_name:
						break
					index += 1
				# URI is an f-string that looks like "finance://ey/{ticker}"
				uri = function_uris[index]
				trimmed_uri = uri[:len(uri)-8] + arguments.get("ticker")
				print (trimmed_uri)

				resource_call_result = await client.read_resource(trimmed_uri)

				# Send all the messages back to the LLM's context, including the data from the tool/resource call
				messages.append(response.choices[0].message) # The LLM's tool_call message from earlier, where it expresses that it wants to use a tool/resource
				messages.append({
					"role": "tool",
					"tool_call_id": tool_call.id,
					"content": str(resource_call_result)
				}) # The data returned from when the tool/resource was actually called
				followup = llm_client.chat.completions.create(
					model="gpt-4.1-mini",
					messages=messages,
					tools=functions,
					tool_choice="auto"
				)

				print (followup.choices[0].message.content)

				# To enable more back and forth with the AI, check whether tool_calls in followup.choices[0].message.tool_calls is empty
				# or if the LLM want to use another tool/resource.
			except:
				print ("Something went wrong. Please type a financial question.")
				continue

async def update_tools(mcp_client) -> Client:
	templates = await mcp_client.list_resource_templates()

	for tmp in templates:
		functions.append({
			"type": "function",
			"function": {
				"name": tmp.name,
				"description": tmp.description[2:len(tmp.description)-2],
				"parameters": {
					"type": "object",
					"properties": {"ticker": {"type": "string"}},
					"required": ["ticker"]
				}
			}
		})
		function_uris.append(tmp.uriTemplate)


if __name__ == "__main__":
	asyncio.run(llm_driven_mcp())

