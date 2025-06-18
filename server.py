from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Finance App")


@mcp.resource("finance://ey/{ticker}")
def getEarningsYield(ticker:str) -> dict:
	"""
	Returns the earnings yield (EBIT/EV multiple) for a given stock ticker symbol.
	"""
	url = f"http://localhost:3000/ey/{ticker}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		ey = data.get("earningsYield")
		return {
			"stock": ticker,
			"earningsYield": ey
		}
	else:
		return {"Request failed with status code": response.status_code}


@mcp.resource("finance://rotc/{ticker}")
def getReturnOnTangibleCapital(ticker: str) -> dict:
	"""
	Returns the Return On Tangible Capital for a given stock ticker symbol.
	"""
	url = f"http://localhost:3000/rotc/{ticker}"
	response = requests.get(url)

	if response.ok:
		data = response.json()
		rotc = data.get("returnOnTangibleCapital")
		return {
			"stock": ticker,
			"returnOnTangibleCapital": rotc
		}
	else:
		return {"Request failed with status code": response.status_code}

if __name__ == "__main__":
	# Starts your server over the default STDIO transport
	mcp.run()