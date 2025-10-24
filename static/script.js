document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        url: document.getElementById('url'),
        prompt: document.getElementById('prompt'),
        extractBtn: document.getElementById('extractBtn'),
        results: document.getElementById('results'),
        loadingSpinner: document.getElementById('loadingSpinner'),
        resultsSection: document.getElementById('resultsSection')
    };

    const showLoading = () => elements.loadingSpinner.classList.remove('hidden');
    const hideLoading = () => elements.loadingSpinner.classList.add('hidden');

    const showError = (message) => {
        alert(message);
        hideLoading();
    };

    const formatResult = (result) => {
        try {
            // If result is already a JSON string, parse it
            const parsed = typeof result === 'string' ? JSON.parse(result) : result;
            return JSON.stringify(parsed, null, 2);
        } catch {
            return result; // Return as is if parsing fails
        }
    };

    elements.extractBtn.addEventListener('click', async () => {
        const url = elements.url.value.trim();
        const prompt = elements.prompt.value.trim();

        if (!url || !prompt) {
            showError('Please enter both URL and extraction prompt');
            return;
        }

        showLoading();
        try {
            const response = await axios.post('/scrape-and-parse', {
                url: url,
                parse_description: prompt
            });
            
            // Only display the result part, properly formatted
            const formattedResult = formatResult(response.data.result);
            elements.results.textContent = formattedResult;
            elements.resultsSection.classList.remove('hidden');

            // Send event tracking data
            const API_KEY = process.env.ANALYZR_API_KEY;
            const trackingUrl = "https://getanalyzr.vercel.app/api/events";
            const headers = {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${API_KEY}`
            };

            const eventData = {
                name: "Information Extracted",
                domain: window.location.hostname || 'localhost',
                description: `Extracted information from URL: ${url}`,
                emoji: "🔍",
                fields: [
                    {
                        name: "URL",
                        value: url,
                        inline: true
                    },
                    {
                        name: "Prompt",
                        value: prompt,
                        inline: true
                    }
                ]
            };

            try {
                await axios.post(trackingUrl, eventData, { headers });
                console.log("Event tracking successful");
            } catch (error) {
                console.error("Event tracking error:", error.response ? error.response.data : error.message);
            }
        } catch (error) {
            showError(error.response?.data?.error || 'Failed to extract information');
        } finally {
            hideLoading();
        }
    });
});