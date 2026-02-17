from flask import Flask, render_template_string
    from database.models import init_db, Lead
    
    app = Flask(__name__)
    db = init_db()
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dean's Lead Finder</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .HOT { background-color: #ffebee; border-left: 5px solid red; }
            .WARM { background-color: #fff3e0; border-left: 5px solid orange; }
            body { padding: 20px; background: #f8f9fa; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="mb-4">Handyman Leads (Pittsburg, TX + 200mi)</h2>
            <div class="card shadow">
                <div class="card-body">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Score</th>
                                <th>Title / Need</th>
                                <th>Location</th>
                                <th>Date</th>
                                <th>Link</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for lead in leads %}
                            <tr class="{{ lead.score }}">
                                <td><strong>{{ lead.score }}</strong></td>
                                <td>{{ lead.title }}</td>
                                <td>{{ lead.location }}</td>
                                <td>{{ lead.date_posted }}</td>
                                <td><a href="{{ lead.url }}" target="_blank" class="btn btn-sm btn-primary">View Ad</a></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        leads = db.query(Lead).order_by(Lead.score_val.desc()).all()
        return render_template_string(HTML_TEMPLATE, leads=leads)
    
    if __name__ == '__main__':
        app.run(debug=True, port=5000, host='0.0.0.0')
    
