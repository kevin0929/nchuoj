document.addEventListener("DOMContentLoaded", () => {
    const problems = JSON.parse(document.getElementById("problems-data").dataset.problems);
    const homeworkid = document.getElementById("homeworkid-data").dataset.homeworkid;
    const userid = document.getElementById("userid-data").dataset.userid;
    const courseid = document.getElementById("courseid-data").dataset.courseid;

    const perPage = 10;
    const currentPage = 1;

    
    // Partition Problem Table
    function renderTable(page) {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = "";

        const start = (page - 1) * perPage;
        const end = start + perPage;
        const pageData = problems.slice(start, end);

        pageData.forEach(problem => {
            const editUrl = `/problem/${userid}/admin/${courseid}/homework/${homeworkid}/${problem.problemid}/edit`;
            const row = `
                <tr class="border-b hover:bg-gray-100 transition duration-200 cursor-pointer"
                    onclick="window.location.href='${editUrl}'">
                    <td class="py-2 px-4">${problem.problemid}</td>
                    <td class="py-2 px-4">${problem.name}</td>
                    <td class="py-2 px-4">${problem.tag}</td>
                    <td class="py-2 px-4">
                        <button data-pid="${problem.problemid}" class="edit-btn text-blue-600 hover:underline mr-2"
                            onclick="window.location.href='${editUrl}'">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-pid="${problem.problemid}" class="delete-btn text-red-600 hover:underline">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });


        // Combine btn to event (delete)
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                const pid = e.currentTarget.dataset.pid;
                const problem = problems.find(p => p.problemid == pid);
                if (confirm(`Are you sure you want to delete problem : ${problem.name}?`)) {
                    deleteProblem(pid);
                }
            });
        });
    }

    function renderPagination(totalPages) {
        const pagination = document.getElementById("pagination");
        pagination.innerHTML = "";

        for (let i=1;i<=totalPages;i++) {
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
        renderPagination(Math.ceil(problems.length / perPage));
    }

    renderTable(currentPage);
    renderPagination(Math.ceil(problems.length / perPage));

    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    async function deleteProblem(problemid) {
        var deleteProblemUrl = `/problem/${userid}/admin/${courseid}/homework/${homeworkid}/${problemid}`;

        try {
            const response = await fetch(deleteProblemUrl, {
                method: "DELETE",
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                }
            });

            const result = await response.json();
            if (result.success) {
                alert("刪除成功!");
                window.location.href = result.redirectUrl;
            } else {
                alert("刪除失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("刪除失敗，請稍後再試！");
        }
    }
})