document.addEventListener("DOMContentLoaded", () => {
    const users = JSON.parse(document.getElementById("users-data").dataset.users);

    // DOM Elements
    const tableBody = document.querySelector("table tbody");
    const editUserModal = document.getElementById("edit-user-modal");
    const editUserForm = document.getElementById("edit-user-form");
    const editUidInput = document.getElementById("edit-uid");
    const editUsernameInput = document.getElementById("edit-username");
    const editEmailInput = document.getElementById("edit-email");
    const editRoleInput = document.getElementById("edit-role");

    // Imporr and add user elements
    const importCsvBtn = document.getElementById("import-csv-btn");
    const addUserBtn = document.getElementById("add-user-btn");
    const importCsvModal = document.getElementById("import-csv-modal");
    const addUserModal = document.getElementById("add-user-modal");
    const cancelImport = document.getElementById("cancel-import");
    const cancelAdd = document.getElementById("cancel-add");
    const cancelEdit = document.getElementById("cancel-edit");

    // For page partition
    const perPage = 10;
    let currentPage = 1;

    // Show Import CSV Modal
    importCsvBtn.addEventListener("click", () => {
        importCsvModal.classList.remove("hidden");
    });

    // Show Add User Modal
    addUserBtn.addEventListener("click", () => {
        addUserModal.classList.remove("hidden");
    });

    // Show Edit User Modal
    function openEditModal(user) {
        // Fill form information
        editUidInput.value = user.userid;
        editUsernameInput.value = user.username;
        editEmailInput.value = user.email;
        editRoleInput.value = user.role;
    
        editUserModal.classList.remove("hidden");
    }

    // Close Modals
    cancelImport.addEventListener("click", () => {
        importCsvModal.classList.add("hidden");
    });

    cancelAdd.addEventListener("click", () => {
        addUserModal.classList.add("hidden");
    });

    cancelEdit.addEventListener("click", () => {
        editUserModal.classList.add("hidden");
    })

    // Populate User Table
    function renderTable(page) {
        const tbody = document.querySelector("tbody");
        tableBody.innerHTML = "";

        const start = (page - 1) * perPage;
        const end = start + perPage;
        const pageData = users.slice(start, end);

        pageData.forEach(user => {
            const row = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${user.userid}</td>
                    <td class="py-2 px-4">${user.username}</td>
                    <td class="py-2 px-4">${user.email}</td>
                    <td class="py-2 px-4">${user.role}</td>
                    <td class="py-2 px-4">
                        <button data-uid="${user.userid}" class="edit-btn text-blue-600 hover:underline mr-2">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-uid="${user.userid}" class="delete-btn text-red-600 hover:underline">
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


    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }


    // Post CSV file to route "/user/import"
    document.getElementById("import-csv-form").addEventListener("submit", async(e) => {
        e.preventDefault();     // prevent default action
        const fileInput = document.getElementById("csv-file").files[0];

        if (!fileInput) {
            alert("請選擇要上傳的 CSV 檔!");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput);

        try {
            const response = await fetch("/user/import", {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert("上傳成功!");
                // importCsvModal.classList.add('hidden');
                window.location.href = result.redirectUrl;
            } else {
                alert("上傳失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }
    })

    // Post add user form to route "/user/add"
    document.getElementById("add-user-form").addEventListener("submit", async(e) => {
        e.preventDefault();

        const username = document.getElementById("edit-username").value;
        const password = document.getElementById("add-password").value;
        const email = document.getElementById("add-email").value;
        const fullname = document.getElementById("add-fullname").value;
        const role = document.getElementById("add-role").value;

        // generate form data
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);
        formData.append("email", email);
        formData.append("fullname", fullname);
        formData.append("role", role);

        try {
            const response = await fetch("/user/add", {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert("上傳成功!");
                addUserModal.classList.add('hidden');
                window.location.href = result.redirectUrl;
            } else {
                alert("上傳失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }
    })

    // Post edit user form to route "/user/<userid>/edit"
    document.getElementById("edit-user-form").addEventListener("submit", async(e) => {
        e.preventDefault();

        const userid = document.getElementById("edit-uid").value
        const username = document.getElementById("edit-username").value;
        const password = document.getElementById("edit-password").value;
        const email = document.getElementById("edit-email").value;
        const role = document.getElementById("edit-role").value;

        // generate form data
        const formData = new FormData();
        formData.append("userid", userid);
        formData.append("username", username);
        formData.append("password", password);
        formData.append("email", email);
        formData.append("role", role);

        const editUserUrl = `/user/${userid}/edit`;
        try {
            const response = await fetch(editUserUrl, {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert("更改成功!");
                editUserModal.classList.add('hidden');
                window.location.href = result.redirectUrl;
            } else {
                alert("更改失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }
    })

    // If confirm, post userid to route "/user/<userid>/delete"
    async function deleteUser(userid) {
        const deleteUserUrl = `/user/${userid}`;

        try {
            const response = await fetch(deleteUserUrl, {
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
});
