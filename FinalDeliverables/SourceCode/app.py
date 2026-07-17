"""
Flask Application for Strategic Product Placement Analysis
============================================================
This is the main Flask application that serves the web interface
for the Strategic Product Placement Analysis project.

Features:
- Home page with project overview
- Dashboard page with embedded Tableau dashboard
- Story page with embedded Tableau story
- About page with project information

Author: Data Analysis Team
Date: 2026
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    'FLASK_SECRET_KEY', 'strategic-product-placement-2026'
)

# Base configuration with valid production/public fallback URLs
TABLEAU_DASHBOARD_URL = os.environ.get(
    'TABLEAU_DASHBOARD_URL',
    'https://www.tableau.com'
)
TABLEAU_STORY_URL = os.environ.get(
    'TABLEAU_STORY_URL',
    'https://www.tableau.com'
)


def get_project_root():
    """Get the project root directory."""
    return os.path.dirname(os.path.abspath(__file__))


def load_data():
    """
    Load the cleaned dataset and compute KPIs.

    Returns:
        tuple: (DataFrame, dict of KPIs)
    """
    project_root = get_project_root()
    filepath = os.path.join(project_root, 'data', 'cleaned',
                            'product_positioning_sales_cleaned.csv')

    if not os.path.exists(filepath):
        # Fallback to raw data
        filepath = os.path.join(project_root, 'data', 'raw',
                                'product_positioning_sales.csv')

    df = pd.read_csv(filepath)

    # Calculate KPIs
    kpis = {
        'total_records': int(len(df)),
        'total_sales': int(df['Sales_Volume'].sum()),
        'avg_sales': round(float(df['Sales_Volume'].mean()), 2),
        'avg_price': round(float(df['Price'].mean()), 2),
        'avg_competitor_price': round(float(df['Competitor_Price'].mean()), 2),
        'categories': int(df['Product_Category'].nunique()),
        'promo_rate': round(
            float((df['Promotion'] == 'Yes').sum() / len(df) * 100), 1
        ),
        'top_category': str(
            df.groupby('Product_Category')['Sales_Volume'].mean().idxmax()
        ),
        'best_position': str(
            df.groupby('Product_Position')['Sales_Volume'].mean().idxmax()
        ),
        'top_demographic': str(
            df.groupby('Consumer_Demographics')['Sales_Volume'].mean().idxmax()
        ),
    }

    return df, kpis


@app.route('/')
def home():
    """
    Home page route.
    Displays project overview, KPIs, and key insights.
    """
    try:
        df, kpis = load_data()
    except Exception as e:
        kpis = {
            'total_records': 0, 'total_sales': 0, 'avg_sales': 0,
            'avg_price': 0, 'avg_competitor_price': 0, 'categories': 0,
            'promo_rate': 0, 'top_category': 'N/A',
            'best_position': 'N/A', 'top_demographic': 'N/A'
        }
    return render_template('index.html', kpis=kpis)


@app.route('/dashboard')
def dashboard():
    """
    Dashboard page route.
    Embeds the Tableau interactive dashboard.
    """
    return render_template(
        'dashboard.html',
        tableau_url=TABLEAU_DASHBOARD_URL
    )


@app.route('/story')
def story():
    """
    Story page route.
    Embeds the Tableau story presentation.
    """
    return render_template(
        'story.html',
        tableau_url=TABLEAU_STORY_URL
    )


@app.route('/about')
def about():
    """
    About page route.
    Displays project information and team details.
    """
    return render_template('about.html')


@app.route('/api/kpis')
def api_kpis():
    """
    API endpoint to retrieve KPIs as JSON.

    Returns:
        JSON: Key Performance Indicators.
    """
    try:
        _, kpis = load_data()
        return jsonify({'status': 'success', 'data': kpis})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/data')
def api_data():
    """
    API endpoint to retrieve the dataset summary as JSON.

    Returns:
        JSON: Dataset summary including head, shape, and column info.
    """
    try:
        df, _ = load_data()
        summary = {
            'shape': {'rows': df.shape[0], 'columns': df.shape[1]},
            'columns': list(df.columns),
            'head': df.head(10).to_dict(orient='records'),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        }
        return jsonify({'status': 'success', 'data': summary})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Strategic Product Placement Analysis")
    print("  Flask Web Application")
    print("=" * 50)
    print("\n  Starting server at http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
