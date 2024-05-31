@app.route('/details/<project>')
def details(project):
    project = data[project]
    return render_template('portfolio-details.html', project=project)