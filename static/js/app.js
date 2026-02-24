document.addEventListener('DOMContentLoaded', () => {
    const planBtn = document.getElementById('planBtn');
    const promptInput = document.getElementById('prompt');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');
    const btnText = document.querySelector('.btn-text');
    const btnSpinner = document.querySelector('.btn-spinner');
    const copyBtn = document.getElementById('copyBtn');

    let rawOutput = '';

    planBtn.addEventListener('click', async () => {
        const promptText = promptInput.value.trim();
        if (!promptText) {
            alert("Please enter your trip details.");
            return;
        }

        // Show loading state
        planBtn.disabled = true;
        btnText.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
        resultCard.classList.add('hidden');

        try {
            const response = await fetch('/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: promptText })
            });

            const data = await response.json();

            if (response.ok) {
                rawOutput = data.result;
                // Parse markdown into HTML safely using marked.js
                resultContent.innerHTML = marked.parse(rawOutput);
                resultCard.classList.remove('hidden');
                
                // Scroll to result smoothly
                resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                alert(`Error: ${data.error || 'Failed to plan trip.'}`);
            }
        } catch (err) {
            console.error(err);
            alert("Network error, please try again later.");
        } finally {
            // Revert loading state
            planBtn.disabled = false;
            btnText.classList.remove('hidden');
            btnSpinner.classList.add('hidden');
        }
    });

    // Copy to clipboard functionality
    copyBtn.addEventListener('click', async () => {
        if (!rawOutput) return;

        try {
            await navigator.clipboard.writeText(rawOutput);
            
            // Temporary icon feedback
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy', err);
        }
    });
});
