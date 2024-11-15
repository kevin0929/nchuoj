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


    // show modal
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        submitModal.classList.remove('hidden');
    });

    // click cancel button and hide modal
    cancelButton.addEventListener('click', function() {
        submitModal.classList.add('hidden');
    });

    // select code option
    codeOption.addEventListener('click', function() {
        codeSection.classList.remove('hidden');
        fileSection.classList.add('hidden');
        codeOption.classList.add('border-b-2', 'border-blue-600', 'text-blue-600', 'font-semibold');
        fileOption.classList.remove('border-b-2', 'border-blue-600', 'text-blue-600', 'font-semibold');
        fileOption.classList.add('text-gray-600');
    });

    // select file option
    fileOption.addEventListener('click', function() {
        fileSection.classList.remove('hidden');
        codeSection.classList.add('hidden');
        fileOption.classList.add('border-b-2', 'border-blue-600', 'text-blue-600', 'font-semibold');
        codeOption.classList.remove('border-b-2', 'border-blue-600', 'text-blue-600', 'font-semibold');
        codeOption.classList.add('text-gray-600');
    });

    // 確認提交操作
    confirmSubmitButton.addEventListener('click', async function() {
        const submitUrl = `/problem/${problemId}/submit`;

        const formData = new FormData();
        formData.append('courseid', courseId);
        // submit the data of code field
        if (!codeSection.classList.contains('hidden')) {
            const language = document.getElementById('languageCode').value;
            const code = document.getElementById('codeInput').value;

            formData.append('type', 'code');
            formData.append('language', language);
            formData.append('code', code);
        }
        else if (!fileSection.classList.contains('hidden')) {
            const language = document.getElementById('languageCode').value;
            const file = document.getElementById('fileInput').files[0];

            formData.append('type', 'file');
            formData.append('language', language);
            formData.append('content', file);
        }

        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

        // Post to submitUrl
        try {
            const response = await fetch(submitUrl, {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData
            });

            const result = await response.json();
            if (result.success) {
                alert("提交成功！");
                window.location.href = result.redirectUrl;
                submitModal.classList.add('hidden');
            } else {
                console.log(result.success);
                alert("提交失敗：" + result.msg);
            }
        } catch (error) {
            console.error("提交錯誤:", error);
            alert("提交失敗，請稍後再試！");
        }
    });
});
