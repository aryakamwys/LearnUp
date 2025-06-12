document.addEventListener('DOMContentLoaded', () => {
    const courseForm = document.getElementById('courseForm');
    const coursesList = document.getElementById('coursesList');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    let courses = [];

    loadCourses();

    courseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const courseId = document.getElementById('courseId').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const content = document.getElementById('content').value;

        try {
            if (courseId) {
                await updateCourse(courseId, { title, description, content });
                resetForm();
                await loadCourses();
            } else {
                const newCourse = await createCourse({ title, description, content });
                courses.push(newCourse);
                displayCourses();
                resetForm();
            }
        } catch (error) {
            console.error(error);
            alert("Error: " + error.message);
        }
    });

    cancelBtn.addEventListener('click', resetForm);

    async function graphqlRequest(query, variables = {}) {
        const res = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, variables })
        });

        if (!res.ok) throw new Error("Network error: " + res.status);

        const json = await res.json();
        if (json.errors) throw new Error(json.errors.map(e => e.message).join('\n'));
        if (!json.data) throw new Error("No data in GraphQL response.");
        return json.data;
    }

    async function loadCourses() {
        const query = `
            query {
                allCourses {
                    id
                    title
                    description
                    content
                }
            }
        `;
        const data = await graphqlRequest(query);
        courses = data.allCourses;
        displayCourses();
    }

    async function createCourse(input) {
        const mutation = `
            mutation($input: CreateCourseInput!) {
                createCourse(input: $input) {
                    id
                    title
                    description
                    content
                }
            }
        `;
        const data = await graphqlRequest(mutation, { input });
        return data.createCourse;
    }

    async function updateCourse(id, inputData) {
        const mutation = `
            mutation($input: UpdateCourseInput!) {
                updateCourse(input: $input) {
                    id
                }
            }
        `;
        await graphqlRequest(mutation, {
            input: { id, ...inputData }
        });
    }

    async function deleteCourse(id) {
        const mutation = `
            mutation($id: ID!) {
                deleteCourse(id: $id)
            }
        `;
        await graphqlRequest(mutation, { id });
    }

    function displayCourses() {
        coursesList.innerHTML = '';
        courses.forEach(course => {
            const el = document.createElement('div');
            el.className = 'bg-white p-4 rounded-xl shadow hover:shadow-lg transition';

            el.innerHTML = `
                <a href="/course.html?id=${course.id}" class="block">
                    <h3 class="text-lg font-semibold text-blue-700 hover:underline cursor-pointer mb-1">
                        ${course.title}
                    </h3>
                </a>
                <p class="text-sm text-gray-600">${course.description}</p>
                <div class="flex gap-2 mt-4">
                    <button onclick="editCourse('${course.id}')" class="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700">Edit</button>
                    <button onclick="deleteCourseHandler('${course.id}')" class="px-3 py-1 bg-red-700 text-white rounded hover:bg-red-600">Delete</button>
                </div>
            `;

            coursesList.appendChild(el);
        });
    }

    window.editCourse = function (id) {
        const course = courses.find(c => c.id == id);
        if (course) {
            document.getElementById('courseId').value = course.id;
            document.getElementById('title').value = course.title;
            document.getElementById('description').value = course.description;
            document.getElementById('content').value = course.content;
            submitBtn.textContent = 'Update Course';
            cancelBtn.classList.remove('hidden');
        }
    };

    window.deleteCourseHandler = async function (id) {
        if (confirm("Delete this course?")) {
            try {
                await deleteCourse(id);
                await loadCourses();
            } catch (err) {
                console.error(err);
                alert("Error during deletion: " + err.message);
            }
        }
    };

    function resetForm() {
        courseForm.reset();
        document.getElementById('courseId').value = '';
        submitBtn.textContent = 'Add Course';
        cancelBtn.classList.add('hidden');
    }
});
