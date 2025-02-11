document.addEventListener("DOMContentLoaded", () => {
    const course_users = JSON.parse(document.getElementById("course-users-data").dataset.courseusers);
    const users = JSON.parse(document.getElementById("users-data").dataset.users);
    const courseid = document.getElementById("courseid-data").dataset.courseid;

    // Show modal
    document.getElementById('add-user-btn').addEventListener('click', function() {
        document.getElementById('add-user-modal').classList.remove('hidden');
        renderUserList('');
    });

    // Hide modal
    document.getElementById('close-modal').addEventListener('click', function() {
        document.getElementById('add-user-modal').classList.add('hidden');
    });

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
                        <!--
                        <button data-cuid="${course_user.cu_id}" class="edit-btn text-blue-600 hover:underline mr-2">
                            <i class="fas fa-edit"></i>
                        </button>
                        -->
                        <button data-cuid="${course_user.cu_id}" class="delete-btn text-red-600 hover:underline">
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
                const cuId = e.currentTarget.dataset.cuid;
                if (confirm(`Are you sure you want to delete user ${cuId}?`)) {
                    deleteCourseUser(cuId);
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

    // -----------------------------
    // Modal search / select user
    // -----------------------------
    const userListEl = document.getElementById('user-list');
    const searchUserInput = document.getElementById('search-user');
    const selectedUserListEl = document.getElementById('selected-user-list');
    let selectedUsers = {};

    // Render Modal user list
    function renderUserList(filter = '') {
        userListEl.innerHTML = "";
        const filteredUsers = users.filter(user => {
            const searchText = filter.toLowerCase();
            return user.username.toLowerCase().includes(searchText) ||
                   user.full_name.toLowerCase().includes(searchText);
        });
        filteredUsers.forEach(user => {
            const li = document.createElement('li');
            li.className = 'user-item cursor-pointer hover:bg-gray-100 px-2 py-1';
            li.textContent = `${user.full_name} (${user.username})`;
            li.dataset.userid = user.userid;
            li.addEventListener('click', function() {
                if (!selectedUsers[user.userid]) {
                    selectedUsers[user.userid] = user;
                    renderSelectedUsers();
                }
            });
            userListEl.appendChild(li);
        });
    }

    function renderSelectedUsers() {
        selectedUserListEl.innerHTML = "";
        Object.values(selectedUsers).forEach(user => {
            const li = document.createElement('li');
            li.className = 'flex justify-between items-center bg-gray-200 px-2 py-1 rounded';
            li.textContent = `${user.full_name} (${user.username})`;
            const removeBtn = document.createElement('button');
            removeBtn.textContent = '移除';
            removeBtn.className = 'text-red-500 ml-2';
            removeBtn.addEventListener('click', function() {
                delete selectedUsers[user.userid];
                renderSelectedUsers();
            });
            li.appendChild(removeBtn);
            selectedUserListEl.appendChild(li);
        });
    }

    searchUserInput.addEventListener('input', function() {
        renderUserList(searchUserInput.value);
    });

    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    document.getElementById('confirm-add-users').addEventListener('click', async function() {
        const selectedUsersArray = Object.values(selectedUsers);
        if (selectedUsersArray.length === 0) {
            alert('請先選擇至少一位使用者');
            return;
        }
        
        const formData = new FormData();
        formData.append("course_users", JSON.stringify({course_users: selectedUsersArray}));
        formData.append("courseid", courseid);

        const addUrl = "/course_user/add";
        try {
            const response = await fetch(addUrl, {
                method: 'POST',
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token') 
                },
                body: formData
            });
            
            const result = await response.json();
            if (result.success) {
                alert("上傳成功!");
                document.getElementById('add-user-modal').classList.remove('hidden');
                window.location.href = result.redirectUrl;
            } else {
                alert("上傳失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }

        selectedUsers = {};
        renderSelectedUsers();
        document.getElementById('add-user-modal').classList.add('hidden');
    });

    async function deleteCourseUser(cuId) {
        const deleteCourseUserUrl = `/course_user/delete/${cuId}`;

        try {
            const response = await fetch(deleteCourseUserUrl, {
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
