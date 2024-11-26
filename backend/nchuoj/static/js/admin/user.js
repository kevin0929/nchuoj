document.addEventListener("DOMContentLoaded", () => {
    const usersData = JSON.parse(document.getElementById("users-data").dataset.users);

    // DOM Elements
    const tableBody = document.querySelector("table tbody");
    const pagination = document.getElementById("pagination");
    const editUserModal = document.getElementById("edit-user-modal");
    const editUserForm = document.getElementById("edit-user-form");
    const cancelEditButton = document.getElementById("cancel-edit");
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

    // Show Import CSV Modal
    importCsvBtn.addEventListener("click", () => {
        importCsvModal.classList.remove("hidden");
    });

    // Show Add User Modal
    addUserBtn.addEventListener("click", () => {
        addUserModal.classList.remove("hidden");
    });

    // Close Modals
    cancelImport.addEventListener("click", () => {
        importCsvModal.classList.add("hidden");
    });

    cancelAdd.addEventListener("click", () => {
        addUserModal.classList.add("hidden");
    });

    // Prevent default form submission for testing purposes
    document.getElementById("import-csv-form").addEventListener("submit", (e) => {
        e.preventDefault();
        alert("CSV uploaded!");
        importCsvModal.classList.add("hidden");
    });

    document.getElementById("add-user-form").addEventListener("submit", (e) => {
        e.preventDefault();
        alert("User added!");
        addUserModal.classList.add("hidden");
    });

    // Populate User Table
    function populateTable(users) {
        tableBody.innerHTML = ""; // Clear previous rows
        users.forEach(user => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${user.userid}</td>
                    <td class="py-2 px-4">${user.username}</td>
                    <td class="py-2 px-4">${user.email}</td>
                    <td class="py-2 px-4">${user.role}</td>
                    <td class="py-2 px-4">
                        <button data-uid="${user.userid}" class="edit-btn text-blue-600 hover:underline mr-2">Edit</button>
                        <button data-uid="${user.userid}" class="delete-btn text-red-600 hover:underline">Delete</button>
                    </td>
                </tr>
            `;

            tableBody.appendChild(row);
        });

        attachEventListeners(); // Attach event listeners for buttons
    }

    // Open Edit User Modal
    function openEditModal(user) {
        editUidInput.value = user.userid;
        editUsernameInput.value = user.username;
        editEmailInput.value = user.email;
        editRoleInput.value = user.role;

        editUserModal.classList.remove("hidden");
    }

    // Close Edit User Modal
    function closeEditModal() {
        editUserModal.classList.add("hidden");
        editUserForm.reset();
    }

    // Handle Edit Button Click
    function handleEditClick(e) {
        const uid = e.target.dataset.userid;
        const user = usersData.find(u => u.userid === uid);
        if (user) {
            openEditModal(user);
        }
    }

    // Handle Delete Button Click
    function handleDeleteClick(e) {
        const uid = e.target.dataset.userid;
        if (confirm(`Are you sure you want to delete user ${uid}?`)) {
            // Optionally, remove the user from the table and usersData
            const userIndex = usersData.findIndex(u => u.userid === uid);
            if (userIndex > -1) {
                usersData.splice(userIndex, 1);
                populateTable(usersData);
            }
        }
    }

    // Handle Form Submit (Edit User)
    editUserForm.addEventListener("submit", e => {
        e.preventDefault();

        const updatedUser = {
            uid: editUidInput.value,
            username: editUsernameInput.value,
            email: editEmailInput.value,
            role: editRoleInput.value
        };

        // Replace with an actual PATCH/PUT request to your API
        console.log("User updated:", updatedUser);

        // Update local usersData and re-render table
        const userIndex = usersData.findIndex(u => u.userid === updatedUser.uid);
        if (userIndex > -1) {
            usersData[userIndex] = updatedUser;
            populateTable(usersData);
        }

        closeEditModal();
    });

    // Attach Event Listeners to Buttons
    function attachEventListeners() {
        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.addEventListener("click", handleEditClick);
        });

        document.querySelectorAll(".delete-btn").forEach(btn => {
            btn.addEventListener("click", handleDeleteClick);
        });
    }

    // Pagination (Placeholder, can be enhanced)
    function setupPagination() {
        // Simple example for demonstration
        pagination.innerHTML = `
            <button class="px-3 py-1 border rounded bg-gray-200 hover:bg-gray-300">Previous</button>
            <button class="px-3 py-1 border rounded bg-gray-200 hover:bg-gray-300">Next</button>
        `;
    }

    // Cancel Edit Modal
    cancelEditButton.addEventListener("click", closeEditModal);

    // Initialize Table
    populateTable(usersData);
    setupPagination();

    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }


    // Post input file to route
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
            if (response.success) {
                alert("上傳成功!");
                window.location.href = result.redirectUrl;
                submitModal.classList.add('hidden');
            } else {
                alert("上傳失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }
    })
});
