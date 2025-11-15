// Main JavaScript for spell correction frontend

// Load backend info and dataset stats on page load
document.addEventListener('DOMContentLoaded', function() {
    loadBackendInfo();
    loadDatasetStats();
});

/**
 * Load and display backend information
 */
async function loadBackendInfo() {
    try {
        const response = await fetch('/api/info');
        const data = await response.json();
        
        const backendInfo = document.getElementById('backendInfo');
        backendInfo.innerHTML = `
            <strong>Backend:</strong> ${data.backend} 
            <span style="color: #10b981;">● ${data.status}</span>
        `;
    } catch (error) {
        console.error('Error loading backend info:', error);
    }
}

/**
 * Correct spelling of the input text
 */
async function correctSpelling() {
    const inputText = document.getElementById('inputText').value.trim();
    const correctBtn = document.getElementById('correctBtn');
    const outputSection = document.getElementById('outputSection');
    const outputText = document.getElementById('outputText');
    
    if (!inputText) {
        alert('Please enter some text to correct!');
        return;
    }
    
    // Show loading state
    correctBtn.disabled = true;
    correctBtn.innerHTML = '<span class="spinner"></span> Correcting...';
    outputText.className = 'output-text placeholder';
    outputText.textContent = 'Processing...';
    
    try {
        const response = await fetch('/api/correct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText })
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const data = await response.json();
        
        // Display corrected text
        outputSection.classList.add('has-content');
        outputText.className = 'output-text';
        outputText.textContent = data.corrected;
        
        // Show a subtle animation
        outputSection.style.animation = 'none';
        setTimeout(() => {
            outputSection.style.animation = '';
        }, 10);
        
    } catch (error) {
        console.error('Error:', error);
        outputText.className = 'output-text';
        outputText.textContent = 'Error: Could not correct text. Please try again.';
        outputText.style.color = '#ef4444';
    } finally {
        // Reset button state
        correctBtn.disabled = false;
        correctBtn.innerHTML = '🔍 Correct Spelling';
    }
}

/**
 * Clear all text fields
 */
function clearAll() {
    document.getElementById('inputText').value = '';
    const outputSection = document.getElementById('outputSection');
    const outputText = document.getElementById('outputText');
    
    outputSection.classList.remove('has-content');
    outputText.className = 'output-text placeholder';
    outputText.textContent = 'Corrected text will appear here...';
    outputText.style.color = '';
}

/**
 * Load an example into the input field
 */
function loadExample(exampleText) {
    document.getElementById('inputText').value = exampleText;
    document.getElementById('inputText').focus();
}

/**
 * Allow Enter key to trigger correction (Ctrl+Enter for newline)
 */
document.getElementById('inputText').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
        e.preventDefault();
        correctSpelling();
    }
});

// ===== Dataset Showcase Functions =====

/**
 * Switch between tabs in the dataset showcase
 */
function switchTab(tabName) {
    // Update tab buttons
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

/**
 * Load and display dataset statistics
 */
async function loadDatasetStats() {
    try {
        const response = await fetch('/api/dataset/stats');
        const data = await response.json();
        
        const statsContent = document.getElementById('statsContent');
        statsContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${data.total_entries}</div>
                    <div class="stat-label">Total Typos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.single_word_typos}</div>
                    <div class="stat-label">Single Word</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.multi_word_typos}</div>
                    <div class="stat-label">Multi Word</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.avg_words_per_typo}</div>
                    <div class="stat-label">Avg Words/Typo</div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3 style="color: #333; margin-bottom: 15px;">📌 Typo Type Distribution</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${data.typo_types.missing_letters}</div>
                        <div class="stat-label">Missing Letters</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.typo_types.extra_letters}</div>
                        <div class="stat-label">Extra Letters</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.typo_types.wrong_letters}</div>
                        <div class="stat-label">Wrong Letters</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3 style="color: #333; margin-bottom: 15px;">🔝 Most Common Words in Typos</h3>
                <div style="background: #f9fafb; padding: 20px; border-radius: 10px;">
                    ${data.common_words.map(item => `
                        <span style="display: inline-block; margin: 5px; padding: 8px 15px; background: white; border-radius: 20px; border: 2px solid #e0e0e0;">
                            <strong>${item.word}</strong> (${item.count})
                        </span>
                    `).join('')}
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading dataset stats:', error);
        document.getElementById('statsContent').innerHTML = 
            '<p style="color: #ef4444;">Error loading statistics</p>';
    }
}

/**
 * Load and display random samples from the dataset
 */
async function loadRandomSamples() {
    const count = document.getElementById('sampleCount').value;
    const samplesContent = document.getElementById('samplesContent');
    
    samplesContent.innerHTML = '<p style="color: #999; text-align: center;">Loading samples...</p>';
    
    try {
        const response = await fetch(`/api/dataset/samples?count=${count}`);
        const data = await response.json();
        
        if (data.samples.length === 0) {
            samplesContent.innerHTML = '<p style="color: #999;">No samples available</p>';
            return;
        }
        
        let matchCount = data.samples.filter(s => s.matches).length;
        let matchRate = ((matchCount / data.samples.length) * 100).toFixed(1);
        
        samplesContent.innerHTML = `
            <div style="background: #f0f4ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <strong>Match Rate:</strong> ${matchCount}/${data.samples.length} (${matchRate}%) 
                <span style="margin-left: 10px;">✅ = TextBlob matches expected | ❌ = Different correction</span>
            </div>
            <div class="sample-grid">
                ${data.samples.map(sample => `
                    <div class="sample-item ${sample.matches ? 'match' : 'mismatch'}">
                        <div style="float: right; font-size: 1.5em;">${sample.matches ? '✅' : '❌'}</div>
                        <div class="sample-typo">❌ Original: "${sample.typo}"</div>
                        <div class="sample-expected">✅ Expected: "${sample.expected}"</div>
                        <div class="sample-textblob">🤖 TextBlob: "${sample.textblob}"</div>
                    </div>
                `).join('')}
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading samples:', error);
        samplesContent.innerHTML = '<p style="color: #ef4444;">Error loading samples</p>';
    }
}

/**
 * Run accuracy test on the dataset
 */
async function testAccuracy() {
    const sampleSize = document.getElementById('accuracySampleSize').value;
    const accuracyBtn = document.getElementById('accuracyBtn');
    const accuracyContent = document.getElementById('accuracyContent');
    
    // Show loading state
    accuracyBtn.disabled = true;
    accuracyBtn.innerHTML = '<span class="spinner"></span> Testing...';
    accuracyContent.innerHTML = '<p style="color: #999; text-align: center;">Running accuracy test...</p>';
    
    try {
        const response = await fetch('/api/dataset/test-accuracy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sample_size: parseInt(sampleSize) })
        });
        
        const data = await response.json();
        
        // Display results
        const correctResults = data.results.filter(r => r.correct);
        const incorrectResults = data.results.filter(r => !r.correct);
        
        accuracyContent.innerHTML = `
            <div class="accuracy-section">
                <h3 style="color: #333; margin-bottom: 10px;">Accuracy Score</h3>
                <div class="accuracy-score">${data.accuracy}%</div>
                <div style="color: #666; margin-bottom: 15px;">
                    ${data.correct_count} correct out of ${data.total_tested} tested
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.accuracy}%;">
                        ${data.accuracy}%
                    </div>
                </div>
            </div>
            
            <details style="margin-top: 20px;">
                <summary style="cursor: pointer; padding: 10px; background: #f0f4ff; border-radius: 5px; font-weight: 600;">
                    ✅ View Correct Corrections (${correctResults.length})
                </summary>
                <div style="margin-top: 10px;" class="sample-grid">
                    ${correctResults.slice(0, 10).map(result => `
                        <div class="sample-item match">
                            <div style="float: right;">✅</div>
                            <div class="sample-typo">❌ "${result.typo}"</div>
                            <div class="sample-expected">✅ "${result.expected}"</div>
                        </div>
                    `).join('')}
                    ${correctResults.length > 10 ? `<p style="text-align: center; color: #666;">... and ${correctResults.length - 10} more</p>` : ''}
                </div>
            </details>
            
            <details style="margin-top: 20px;">
                <summary style="cursor: pointer; padding: 10px; background: #fef2f2; border-radius: 5px; font-weight: 600;">
                    ❌ View Incorrect Corrections (${incorrectResults.length})
                </summary>
                <div style="margin-top: 10px;" class="sample-grid">
                    ${incorrectResults.slice(0, 10).map(result => `
                        <div class="sample-item mismatch">
                            <div style="float: right;">❌</div>
                            <div class="sample-typo">❌ Original: "${result.typo}"</div>
                            <div class="sample-expected">✅ Expected: "${result.expected}"</div>
                            <div class="sample-textblob">🤖 TextBlob: "${result.corrected}"</div>
                        </div>
                    `).join('')}
                    ${incorrectResults.length > 10 ? `<p style="text-align: center; color: #666;">... and ${incorrectResults.length - 10} more</p>` : ''}
                </div>
            </details>
        `;
        
    } catch (error) {
        console.error('Error testing accuracy:', error);
        accuracyContent.innerHTML = '<p style="color: #ef4444;">Error running accuracy test</p>';
    } finally {
        accuracyBtn.disabled = false;
        accuracyBtn.innerHTML = '🎯 Run Accuracy Test';
    }
}
