import { NextResponse } from 'next/server';
import { mastra } from '../../../mastra';

const PR_AGENTS = ['prAgent', 'prAgentSecondary', 'prAgentFallback'] as const;

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { connectionId, owner, repo, file, issue, code_snippet, secure_fix } = body;

        if (!connectionId || !owner || !repo || !file || !issue) {
            return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
        }

        const promptText = `
Please fix the following vulnerability in the repository and create a Pull Request.
Repository: ${owner}/${repo}
File Path: ${file}

Vulnerability Issue: ${issue}
Vulnerable Snippet:
${code_snippet || 'N/A'}

Suggested Secure Fix Strategy:
${secure_fix || 'N/A'}

Use your tools to fetch the file, apply the fix using EXACT snippet replacement (do NOT generate the whole file!), and create the PR.
Connection ID for tools: ${connectionId}
`;

        // Convert to messages array format for Mastra (same as chat API)
        const messages = [
            {
                id: crypto.randomUUID(),
                role: 'user',
                content: promptText,
                createdAt: new Date(),
            }
        ];

        let lastError: Error | null = null;
        for (const agentName of PR_AGENTS) {
            const agent = mastra.getAgent(agentName);
            if (!agent) {
                console.warn(`[Fix Issue] Agent ${agentName} not found`);
                continue;
            }
            try {
                console.log(`[Fix Issue] Attempting with ${agentName}...`);
                const result = await agent.generate(messages as any);
                const responseText = result?.text ?? String(result ?? '');
                if (responseText) {
                    console.log(`[Fix Issue] Success with ${agentName}`);
                    return NextResponse.json({ success: true, message: responseText });
                }
            } catch (err: any) {
                lastError = err;
                console.error(`[Fix Issue] ${agentName} failed:`, err.message);
            }
        }

        throw lastError || new Error("All PR agents failed. Please check your API keys and try again.");
    } catch (error: any) {
        console.error("Fix Issue API Error:", error);
        return NextResponse.json({ error: error.message || "Failed to fix issue" }, { status: 500 });
    }
}
