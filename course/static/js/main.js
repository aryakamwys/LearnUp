document.addEventListener('DOMContentLoaded', () => {
    const courseForm = document.getElementById('courseForm');
    const coursesList = document.getElementById('coursesList');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const addCourseBtn = document.getElementById('addCourseBtn');
    const overlay = document.getElementById('overlay');

    let courses = [];
    let editing = false;

    loadCourses();

    addCourseBtn.addEventListener('click', () => {
        showForm();
        resetForm();
    });

    overlay.addEventListener('click', hideForm);
    cancelBtn.addEventListener('click', hideForm);

    courseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const courseId = document.getElementById('courseId').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const content = document.getElementById('content').value;

        try {
            if (courseId) {
                await updateCourse(courseId, { title, description, content });
                await loadCourses();
                hideForm();
            } else {
                const newCourse = await createCourse({ title, description, content });
                await loadCourses();
                hideForm();
                displayCourses(newCourse.id);
            }
        } catch (error) {
            console.error(error);
            alert("Error: " + error.message);
        }
    });

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

    function displayCourses(highlightId = null) {
        coursesList.innerHTML = '';
        courses.forEach(course => {
            const el = document.createElement('div');
            el.className = 'bg-white p-4 rounded-xl shadow hover:shadow-lg transition flex flex-col';
            if (highlightId && course.id === highlightId) {
                el.classList.add('ring-2', 'ring-indigo-400');
                setTimeout(() => {
                    el.classList.remove('ring-2', 'ring-indigo-400');
                }, 2000);
            }
            el.innerHTML = `
                <a href="/course.html?id=${course.id}" class="block w-fit">
                  <h3 class="text-lg font-semibold text-blue-700 cursor-pointer mb-1 hover:underline">${course.title}</h3>
                </a>
                <p class="text-sm text-gray-600 mb-2">${course.description}</p>
                <div class="flex gap-2 mt-2">
                    <button class="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700" data-edit="${course.id}">Edit</button>
                    <button class="px-3 py-1 bg-red-700 text-white rounded hover:bg-red-600" data-delete="${course.id}">Delete</button>
                </div>
            `;
            el.querySelector('[data-edit]').addEventListener('click', () => {
                editCourse(course.id);
            });
            el.querySelector('[data-delete]').addEventListener('click', async () => {
                if (confirm("Delete this course?")) {
                    try {
                        await deleteCourse(course.id);
                        await loadCourses();
                    } catch (err) {
                        console.error(err);
                        alert("Error during deletion: " + err.message);
                    }
                }
            });
            coursesList.appendChild(el);
            if (highlightId && course.id === highlightId) {
                setTimeout(() => {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 100);
            }
        });
    }

    function editCourse(id) {
        const course = courses.find(c => c.id == id);
        if (course) {
            document.getElementById('courseId').value = course.id;
            document.getElementById('title').value = course.title;
            document.getElementById('description').value = course.description;
            document.getElementById('content').value = course.content;
            submitBtn.textContent = 'Update Course';
            showForm();
        }
    }

    function showForm() {
        courseForm.classList.remove('hidden');
        overlay.classList.remove('hidden');
    }
    function hideForm() {
        courseForm.classList.add('hidden');
        overlay.classList.add('hidden');
        resetForm();
    }
    function resetForm() {
        courseForm.reset();
        document.getElementById('courseId').value = '';
        submitBtn.textContent = 'Save';
    }
});
