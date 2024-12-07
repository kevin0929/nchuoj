document.addEventListener("DOMContentLoaded", () => {
    const homeworks = JSON.parse(document.getElementById("homeworks-data").dataset.homeworks);
    const userid = document.getElementById("userid-data").dataset.userid;
    const courseid = document.getElementById("courseid-data").dataset.courseid;

    const perPage = 10;
    const currentPage = 1;


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
    
    // Partition Course Table
    function renderTable(page) {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = "";

        const start = (page - 1) * perPage;
        const end = start + perPage;
        const pageData = homeworks.slice(start, end);

        pageData.forEach(homework => {
            const startDateFormatted = formatDate(homework.start_date);
            const endDateFormatted = formatDate(homework.end_date);
            const editUrl = `/homework/${userid}/admin/${courseid}/homework/${homework.homeworkid}/edit`;
            const row = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${homework.homeworkid}</td>
                    <td class="py-2 px-4">${homework.name}</td>
                    <td class="py-2 px-4">${startDateFormatted}</td>
                    <td class="py-2 px-4">${endDateFormatted}</td>
                    <td class="py-2 px-4">
                        <button data-hid="${homework.homeworkid}" class="edit-btn text-blue-600 hover:underline mr-2"
                            onclick="window.location.href='${editUrl}'">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-cid="${homework.homeworkid}" class="delete-btn text-red-600 hover:underline">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });

        // document.querySelectorAll(".edit-btn").forEach(button => {
        //     button.addEventListener("click", (e) => {
        //         const cid = e.currentTarget.dataset.cid;
        //         const course = courses.find(c => c.courseid == cid);
        //         openAModal(user);
        //     });
        // });

        // Combine btn to event (delete)
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                const cid = e.currentTarget.dataset.cid;
                const course = courses.find(c => c.courseid == cid);
                if (confirm(`Are you sure you want to delete course : ${course.coursename}?`)) {
                    deleteCourse(cid);
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
        renderPagination(Math.ceil(homeworks.length / perPage));
    }

    renderTable(currentPage);
    renderPagination(Math.ceil(homeworks.length / perPage));

    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
})