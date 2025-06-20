# finance-mcp
MCP server for my financial metrics API, and an MCP client for LLMs that interface with it.

## Overview
In this project I built an MCP server and MCP client that OpenAI's models can use to interface with this [Financial Metrics API](https://github.com/alaapmurali/financial-metrics-app) I built.

For now, the MCP client only works with OpenAI's GPT 4.1 Mini model but I plan to build clients that work with other models and companies.

## Use Cases
Since this project is meant to use the Financial Metrics API as a tool to answer financial questions, I've blocked LLMs from responding to prompts that don't require using this tool. This protects your OpenAI token limit by blocking prompts that can be answered using ChatGPT or another LLM product directly. I plan to build a cleaner solution in due time, but for now this does the job.

To use correctly, make sure your prompts specifically reference earnings yield (or the EBIT/EV multiple) and tangible ROI (or Return on Tangible Investment), since those are the two financial metrics currently supported in the Financial Metrics API. And make sure you're asking about specific companies or a set of companies (e.g. 5 largest market cap companies in healthcare, gpu chip companies, etc.).

The LLM's memory context is update throughout the course of your conversation, so you can referrence older prompts or responses.

### A real question-answer chain using this tool

> [!TIP]
> Although I'm just showing the conversation flow below, when you use the tool you will be able to see the actual tool calls the MCP client makes to the MCP server.

**User:**
`What's the difference between NVIDIA and AMD when it comes to earnings yield and tangible ROI?`

**LLM:**
```
The differences between NVIDIA and AMD in terms of earnings yield and return on tangible capital are as follows:

- Earnings Yield:
  - NVIDIA: Approximately 2.34%
  - AMD: Approximately 1.01%

- Return on Tangible Capital:
  - NVIDIA: Approximately 96.25%
  - AMD: Approximately 11.45%

NVIDIA has a higher earnings yield and a significantly higher return on tangible capital compared to AMD. This suggests that NVIDIA is generating more earnings relative to its enterprise value and also earning a higher return on its tangible capital.
```

**User:**
`Compare the tangible ROI of the 5 largest market cap companies in medical tech.`

**LLM:**
```
The tangible Return on Tangible Capital (ROTC) for the 5 largest medical tech companies by market cap are as follows:

- Medtronic (MDT): 0.0%
- Stryker (SYK): 30.89%
- Intuitive Surgical (ISRG): 14.13%
- Becton Dickinson (BDX): 23.14%
- Abbott Laboratories (ABT): 20.31%

Stryker has the highest tangible ROI among these companies, followed by Becton Dickinson and Abbott Laboratories. Medtronic shows a ROTC of 0.0%, which might indicate no return on tangible capital based on the current data.
```

**User:**
`Compare the 3 largest companies in the GPU chip industry with the 3 largest companies in the med tech industry in terms of earnings yield and tangible ROI.`

**LLM:**
```
Here's the comparison of the 3 largest companies in the GPU chip industry (NVIDIA, AMD, Intel) with the 3 largest companies in the medical tech industry (Medtronic, Stryker, Intuitive Surgical) in terms of earnings yield and return on tangible capital (ROTC):

GPU Chip Industry:
- NVIDIA (NVDA):
  - Earnings Yield: 2.34%
  - Return on Tangible Capital: 96.25%
- AMD (AMD):
  - Earnings Yield: 1.01%
  - Return on Tangible Capital: 11.45%
- Intel (INTC):
  - Earnings Yield: -7.61%
  - Return on Tangible Capital: -7.68%

Medical Tech Industry:
- Medtronic (MDT):
  - Earnings Yield: 0.0%
  - Return on Tangible Capital: 0.0%
- Stryker (SYK):
  - Earnings Yield: 3.03%
  - Return on Tangible Capital: 30.89%
- Intuitive Surgical (ISRG):
  - Earnings Yield: 1.29%
  - Return on Tangible Capital: 14.13%

Summary:
- NVIDIA leads among GPU chip companies with a very high ROTC of 96.25% and a decent earnings yield.
- Stryker leads among medical tech companies with a solid ROTC of 30.89% and strong earnings yield.
- Medtronic shows no earnings yield or ROTC.
- Intel has negative values for both metrics, indicating struggles.
- AMD and Intuitive Surgical have moderate ROTC and earnings yields.

If you want, I can provide more details or comparisons.
```

**User:**
`Now do the same thing you just did, but instead of med tech companies use the 3 biggest banks.`

**LLM:**
```
Here's the comparison of the 3 largest companies in the GPU chip industry with the 3 largest companies in the bank industry in terms of earnings yield and return on tangible capital (ROTC):

GPU Chip Industry:
1. NVIDIA (NVDA)
   - Earnings Yield: 2.34%
   - ROTC: 96.25%
2. AMD (AMD)
   - Earnings Yield: 1.01%
   - ROTC: 11.45%
3. Intel (INTC)
   - Earnings Yield: -7.61%
   - ROTC: -7.68%

Bank Industry:
1. JPMorgan Chase (JPM)
   - Earnings Yield: 7.01%
   - ROTC: 8.68%
2. Bank of America (BAC)
   - Earnings Yield: 4.09%
   - ROTC: 3.85%
3. Wells Fargo (WFC)
   - Earnings Yield: 6.92%
   - ROTC: 5.61%

Summary:
- NVIDIA leads the GPU chip industry with a very high return on tangible capital (96.25%) and moderate earnings yield.
- AMD has a positive but much lower ROTC (11.45%) and lower earnings yield.
- Intel has negative earnings yield and ROTC.
- In the banking sector, JPMorgan Chase has the highest earnings yield and ROTC, but their ROTC is significantly lower than NVIDIA's.
- Overall, the GPU chip companies (especially NVIDIA) exhibit higher ROTC compared to banks, while banks generally show higher earnings yields than most GPU chip companies except Intel which is negative.
```

**User:**
`What can you tell me about the health of the consumer non-cyclicals sector based on the earnings yield and tanbile ROI for a few top companies in that sector?`

**LLM:**
```
For the consumer non-cyclicals sector, looking at some of the top companies:

Procter & Gamble (PG):
- Earnings Yield: 4.79%
- Return on Tangible Capital (ROTC): 75.04%

Coca-Cola (KO):
- Earnings Yield: 4.43%
- ROTC: 33.60%

PepsiCo (PEP):
- Earnings Yield: 6.00%
- ROTC: 36.14%

Analysis:
These companies show relatively strong earnings yields generally in the 4.4% to 6% range, indicating reasonable profitability relative to enterprise value. The ROTC values are particularly notable, with PG showing an exceptionally high 75%, and KO and PEP in the mid 30% range. This suggests these companies are efficient at generating returns on their tangible capital and exhibit good operational performance.

Overall, the consumer non-cyclicals sector, represented by these major companies, appears financially healthy with solid profitability and effective use of tangible capital. This reflects the sector's typically stable demand and consistent cash flow characteristics.
```

## Setup
This is a command line tool--I plan to build a UI at some point.

Make sure you have an API Key for OpenAI's developer platform and store it in a local `.env` file.

Create a Python virtual environment inside the main project directory and run `pip install -r requirements.txt` to install all the project dependencies (they are all Python libraries).

Finally, run `python client.py` to run the tool and to enter your prompt.

Enjoy!
