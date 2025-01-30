document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submitButton');
    const confirmSubmitButton = document.getElementById('confirmSubmit');
    const cancelButton = document.getElementById('cancelButton');
    const submitModal = document.getElementById('submitModal');

    const codeOption = document.getElementById('codeOption');
    const fileOption = document.getElementById('fileOption');
    const codeSection = document.getElementById('codeSection');
    const fileSection = document.getElementById('fileSection');

    const problemId = confirmSubmitButton.dataset.problemId;
    const courseId = confirmSubmitButton.dataset.courseId;

    // build loading area
    const loadingOverlay = document.createElement("div");
    loadingOverlay.id = "loadingOverlay";
    loadingOverlay.classList.add(
        "absolute", "inset-0", "flex", "items-center", "justify-center", "bg-white", "bg-opacity-75", "hidden"
    );
    loadingOverlay.innerHTML = `
        <div class="flex flex-col items-center">
            <div class="w-10 h-10 border-4 border-blue-500 border-dashed rounded-full animate-spin"></div>
            <p class="text-gray-700 font-medium mt-2">Judging...</p>
        </div>
    `;
    submitModal.appendChild(loadingOverlay);

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        submitModal.classList.remove('hidden');
    });

    cancelButton.addEventListener('click', function() {
        submitModal.classList.add('hidden');
        loadingOverlay.classList.add("hidden");
        confirmSubmitButton.disabled = false;
    });

    codeOption.addEventListener('click', function() {
        codeSection.classList.remove('hidden');
        fileSection.classList.add('hidden');
    });

    fileOption.addEventListener('click', function() {
        fileSection.classList.remove('hidden');
        codeSection.classList.add('hidden');
    });

    // get CSRF Token
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // check submit operation
    confirmSubmitButton.addEventListener('click', async function() {
        const submitUrl = `/problem/${problemId}/submit`;

        const formData = new FormData();
        formData.append('courseid', courseId);

        if (!codeSection.classList.contains('hidden')) {
            const language = document.getElementById('languageCode').value;
            const code = document.getElementById('codeInput').value;
            formData.append('type', 'code');
            formData.append('language', language);
            formData.append('code', code);
        } else if (!fileSection.classList.contains('hidden')) {
            const language = document.getElementById('languageFile').value;
            const file = document.getElementById('fileInput').files[0];
            formData.append('type', 'file');
            formData.append('language', language);
            formData.append('content', file);
        }

        // disable button and show loading...
        confirmSubmitButton.disabled = true;
        loadingOverlay.classList.remove("hidden");

        try {
            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData
            });

            const result = await response.json();
            const message = result.message || "Your submission was successfully processed!";
            const redirectUrl = result.redirectUrl || `/problem/${problemId}`;

            // remove loading
            loadingOverlay.classList.add("hidden");

            if (result.success) {
                    window.location.href = redirectUrl;
            } else {
                submitModal.innerHTML = `
                    <div class="text-center p-6">
                        <p class="text-red-600 font-bold text-lg">❌ Submission Failed</p>
                        <p class="text-gray-600">${result.msg || "An unknown error occurred."}</p>
                        <button id="closeErrorModal" class="mt-4 px-4 py-2 bg-gray-500 text-white rounded">Retry</button>
                    </div>
                `;

                document.getElementById("closeErrorModal").addEventListener("click", function () {
                    submitModal.classList.add("hidden");
                    window.location.reload();
                });
            }
        } catch (error) {
            console.error("提交錯誤:", error);
            loadingOverlay.classList.add("hidden");

            submitModal.innerHTML = `
                <div class="text-center p-6">
                    <p class="text-red-600 font-bold text-lg">⚠️ Network Error</p>
                    <p class="text-gray-600">Failed to submit. Please check your internet connection and try again.</p>
                    <button id="closeNetworkError" class="mt-4 px-4 py-2 bg-gray-500 text-white rounded">Close</button>
                </div>
            `;

            document.getElementById("closeNetworkError").addEventListener("click", function () {
                submitModal.classList.add("hidden");
                window.location.reload();
            });
        } finally {
            confirmSubmitButton.disabled = false;
        }
    });
});
