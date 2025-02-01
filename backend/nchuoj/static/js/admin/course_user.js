document.addEventListener("DOMContentLoaded", () => {
    const course_users = JSON.parse(document.getElementById("course-users-data").dataset.courseusers);

    // DOM Elements
    const tableBody = document.querySelector("table tbody");

    // For page partition
    const perPage = 10;
    let currentPage = 1;

    // Populate User Table
    function renderTable(page) {
        const tbody = document.querySelector("tbody");
        tableBody.innerHTML = "";

        const start = (page - 1) * perPage;
        const end = start + perPage;
        const pageData = course_users.slice(start, end);

        pageData.forEach(course_user => {
            const row = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${course_user.cu_id}</td>
                    <td class="py-2 px-4">${course_user.userid}</td>
                    <td class="py-2 px-4">${course_user.username}</td>
                    <td class="py-2 px-4">${course_user.full_name}</td>
                    <td class="py-2 px-4">${course_user.role}</td>
                    <td class="py-2 px-4">
                        <button data-uid="${course_user.userid}" class="edit-btn text-blue-600 hover:underline mr-2">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-uid="${course_user.userid}" class="delete-btn text-red-600 hover:underline">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;

            tbody.innerHTML += row;
        });

        /*
            TODO : 
                1. search user by username
        */

        // Combine btn to event (edit)
        document.querySelectorAll(".edit-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                const uid = e.currentTarget.dataset.uid;
                const user = users.find(u => u.userid == uid);
                openEditModal(user);
            });
        });

        // Combine btn to event (delete)
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                const uid = e.currentTarget.dataset.uid;
                if (confirm(`Are you sure you want to delete user ${uid}?`)) {
                    deleteUser(uid);
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
        renderPagination(Math.ceil(users.length / perPage));
    }

    renderTable(currentPage);
    renderPagination(Math.ceil(users.length / perPage));
});
