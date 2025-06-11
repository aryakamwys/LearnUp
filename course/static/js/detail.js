document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const courseId = params.get('id');

    if (!courseId) {
        document.getElementById('courseDetail').innerHTML = "<p class='text-red-500'>No course ID provided.</p>";
        return;
    }

    try {
        const query = `
            query($id: ID!) {
                course(id: $id) {
                    title
                    description
                    content
                }
            }
        `;
        const res = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, variables: { id: courseId } })
        });

        const { data, errors } = await res.json();
        if (errors) throw new Error(errors.map(e => e.message).join('\n'));

        const course = data.course;
        if (course) {
            document.getElementById('title').textContent = course.title;
            document.getElementById('description').textContent = course.description;
            document.getElementById('content').textContent = course.content;
        } else {
            document.getElementById('courseDetail').innerHTML = "<p class='text-red-500'>Course not found.</p>";
        }

    } catch (err) {
        console.error(err);
        document.getElementById('courseDetail').innerHTML = `<p class='text-red-500'>Error: ${err.message}</p>`;
    }
});
