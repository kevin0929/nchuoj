document.addEventListener("DOMContentLoaded", () => {
    const submissionsData = document.getElementById("submissions-data").dataset.submissions;
    const userData = document.getElementById("user-data").dataset.user;
    const courseData = document.getElementById("course-data").dataset.course;
    const submissions = JSON.parse(submissionsData);
    const user = JSON.parse(userData);
    const course = JSON.parse(courseData);

    const perPage = 10;
    let currentPage = 1;

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString("zh-TW", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    function renderTable(page) {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = "";

        const start = (page - 1) * perPage;
        const end = start + perPage;
        const pageData = submissions.slice(start, end);

        pageData.forEach(submission => {
            const formattedTime = formatDate(submission.submission.submit_time);
            const row = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${submission.submission.submissionid}</td>
                    <td class="py-2 px-4 text-blue-600 hover:underline"> 
                        <a href="/course/${user.userid}/${course.courseid}/homework/${submission.problem.homeworkid}/${submission.submission.problemid}">
                            #${submission.submission.problemid} - ${submission.problem.name}
                        </a>
                    </td>
                    <td class="py-2 px-4">${user.username}</td>
                    <td class="py-2 px-4">
                        <span class="${submission.submission.status === 'Accepted' ? 'text-green-500' : 'text-red-500'}">
                            ${submission.submission.status}
                        </span>
                    </td>
                    <td class="py-2 px-4">${submission.submission.runtime} ms</td>
                    <td class="py-2 px-4">${submission.submission.memory} KB</td>
                    <td class="py-2 px-4">${submission.submission.score}</td>
                    <td class="py-2 px-4">${submission.submission.language}</td>
                    <td class="py-2 px-4">${formattedTime}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }

    function renderPagination(totalPages) {
        const pagination = document.getElementById("pagination");
        pagination.innerHTML = "";

        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement("button");
            button.textContent = i;
            button.className = `px-4 py-2 ${i === currentPage ? "bg-blue-500 text-white" : "bg-gray-200 hover:bg-gray-300"} rounded`;
            button.addEventListener("click", () => {
                changePage(i);
            });
            pagination.appendChild(button);
        }
    }

    function changePage(page) {
        currentPage = page;
        renderTable(page);
        renderPagination(Math.ceil(submissions.length / perPage));
    }

    renderTable(currentPage);
    renderPagination(Math.ceil(submissions.length / perPage));
});
