document.addEventListener("DOMContentLoaded", () => {
    const courses = JSON.parse(document.getElementById("courses-data").dataset.courses);
    const userid = document.getElementById("userid-data").dataset.userid;

    // DOM element
    const addCourseBtn = document.getElementById("add-course-btn");
    const addCourseCancelBtn = document.getElementById("cancel-add");
    const addCourseModal = document.getElementById("add-course-modal");

    const perPage = 10;
    const currentPage = 1;

    // Show add course modal
    addCourseBtn.addEventListener("click", () => {
        addCourseModal.classList.remove("hidden");
    })

    // Close modal
    addCourseCancelBtn.addEventListener("click", () => {
        addCourseModal.classList.add("hidden");
    })


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
        const pageData = courses.slice(start, end);

        pageData.forEach(course => {
            const startDateFormatted = formatDate(course.start_date);
            const endDateFormatted = formatDate(course.end_date);
            const editUrl = `/course/${userid}/admin/${course.courseid}/edit`
            const row = `
                <tr class="border-b hover:bg-gray-100">
                    <td class="py-2 px-4">${course.courseid}</td>
                    <td class="py-2 px-4">${course.coursename}</td>
                    <td class="py-2 px-4">${course.teacher}</td>
                    <td class="py-2 px-4">${startDateFormatted}</td>
                    <td class="py-2 px-4">${endDateFormatted}</td>
                    <td class="py-2 px-4">${course.is_activate}</td>
                    <td class="py-2 px-4">
                        <button data-cid="${course.courseid}" class="edit-btn text-blue-600 hover:underline mr-2"
                            onclick="window.location.href='${editUrl}'">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button data-cid="${course.courseid}" class="delete-btn text-red-600 hover:underline">
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
        renderPagination(Math.ceil(courses.length / perPage));
    }

    renderTable(currentPage);
    renderPagination(Math.ceil(courses.length / perPage));

    // Get cookie name function
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    
    // Post add course form to route "course/" (not done yet)
    document.getElementById("add-course-modal").addEventListener("submit", async(e) => {
        e.preventDefault();

        const coursename = document.getElementById("add-course-name").value;
        const teacher = document.getElementById("add-course-teacher").value;
        const start_date = document.getElementById("add-course-start-date").value;
        const end_date = document.getElementById("add-course-end-date").value;
        const is_activate = document.getElementById("add-course-is-activate").value;

        const formData = new FormData();
        formData.append("coursename", coursename);
        formData.append("teacher", teacher);
        formData.append("start_date", start_date);
        formData.append("end_date", end_date);
        formData.append("is_activate", is_activate);

        const addCourseUrl = `/course/add`;
        try {
            const response = await fetch(addCourseUrl, {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': getCookie('csrf_access_token')
                },
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert("上傳成功!");
                addCourseModal.classList.add('hidden');
                window.location.href = result.redirectUrl;
            } else {
                alert("上傳失敗：" + result.msg);
            }
        } catch (error) {
            console.log(error);
            alert("上傳失敗，請稍後再試！");
        }
    })

    async function deleteCourse(courseid) {
        const deleteCourseUrl = `/course/${courseid}`;
        try {
            const response = await fetch(deleteCourseUrl, {
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