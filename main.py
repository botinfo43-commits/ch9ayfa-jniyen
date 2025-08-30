from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import uuid
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ff-spam-master-dev-jniyen-ch9ayfa-2024')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL for the spam service
SPAM_BASE_URL = "https://spamch9ayfa-production.up.railway.app"

# Data file path
DATA_FILE = 'data.json'

# Load data from JSON file
def load_data():
    """Load spam sessions data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data)} spam sessions from {DATA_FILE}")
                return data
        else:
            logger.info(f"Data file {DATA_FILE} not found, starting with empty data")
            return {}
    except Exception as e:
        logger.error(f"Error loading data from {DATA_FILE}: {str(e)}")
        return {}

# Save data to JSON file
def save_data(data):
    """Save spam sessions data to JSON file"""
    try:
        # Create backup if file exists
        if os.path.exists(DATA_FILE):
            backup_file = f"{DATA_FILE}.backup"
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            except Exception as backup_error:
                logger.warning(f"Could not create backup: {backup_error}")

        # Save new data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(data)} spam sessions to {DATA_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {DATA_FILE}: {str(e)}")
        return False

# Create backup of data
def create_backup():
    """Create a timestamped backup of the data file"""
    try:
        if os.path.exists(DATA_FILE):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"data_backup_{timestamp}.json"
            with open(DATA_FILE, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            logger.info(f"Backup created: {backup_file}")
            return backup_file
        return None
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        return None

# Load initial data
active_spams = load_data()

# Free Fire UID validation
def is_valid_freefire_uid(uid):
    """Validate Free Fire UID format (typically 9-12 digits)"""
    if not uid:
        return False
    # Remove any spaces or special characters
    clean_uid = ''.join(filter(str.isdigit, uid))
    # Free Fire UIDs are typically 9-12 digits
    return len(clean_uid) >= 9 and len(clean_uid) <= 12 and clean_uid.isdigit()

def format_freefire_uid(uid):
    """Format Free Fire UID by removing non-digits"""
    return ''.join(filter(str.isdigit, uid)) if uid else ""

@app.route('/')
def index():
    """Main page with options to start or stop spam"""
    return render_template('index.html')

@app.route('/spam_vip', methods=['GET', 'POST'])
def spam_vip():
    """Handle Free Fire UID spam VIP requests"""
    if request.method == 'POST':
        uid = request.form.get('uid')
        target_uid = request.form.get('target_uid')  # Free Fire UID to spam

        # Validate Free Fire UID
        if target_uid:
            target_uid = format_freefire_uid(target_uid)
            if not is_valid_freefire_uid(target_uid):
                flash('Invalid Free Fire UID format. Please enter a valid 9-12 digit UID.', 'error')
                return render_template('spam_form.html', action='spam_vip', title='Start Free Fire Spam VIP')
        else:
            flash('Free Fire UID is required to start spam.', 'error')
            return render_template('spam_form.html', action='spam_vip', title='Start Free Fire Spam VIP')

        # Generate session UID if not provided
        if not uid:
            uid = f"ff_spam_{uuid.uuid4().hex[:8]}"

        try:
            # Make request to the spam service with Free Fire UID
            spam_url = f"{SPAM_BASE_URL}/spam_vip?id={target_uid}"
            response = requests.get(spam_url, timeout=10)

            if response.status_code == 200:
                # Add to active spams list
                active_spams[uid] = {
                    'session_uid': uid,
                    'target_uid': target_uid,
                    'status': 'active',
                    'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'Free Fire VIP',
                    'game': 'Free Fire'
                }
                # Save data to file
                save_data(active_spams)
                flash(f'Free Fire spam VIP started successfully! Target UID: {target_uid} | Session: {uid}', 'success')
                logger.info(f"Free Fire spam VIP started for target UID: {target_uid}, session: {uid}")
            else:
                flash(f'Failed to start Free Fire spam VIP. Status: {response.status_code}', 'error')
                logger.error(f"Failed to start Free Fire spam VIP for target UID: {target_uid}, Status: {response.status_code}")

        except requests.RequestException as e:
            flash(f'Error connecting to spam service: {str(e)}', 'error')
            logger.error(f"Request error for target UID {target_uid}: {str(e)}")

        return redirect(url_for('index'))

    return render_template('spam_form.html', action='spam_vip', title='Start Free Fire Spam VIP')

@app.route('/stop', methods=['GET', 'POST'])
def stop_spam():
    """Handle stop Free Fire spam requests"""
    if request.method == 'POST':
        session_uid = request.form.get('uid')
        target_uid = request.form.get('target_uid')

        # Check if we have session UID or target UID
        if session_uid and session_uid in active_spams:
            # Use target UID from active session
            target_uid = active_spams[session_uid]['target_uid']
        elif target_uid:
            # Format and validate the provided target UID
            target_uid = format_freefire_uid(target_uid)
            if not is_valid_freefire_uid(target_uid):
                flash('Invalid Free Fire UID format. Please enter a valid 9-12 digit UID.', 'error')
                return render_template('spam_form.html', action='stop', title='Stop Free Fire Spam')
        else:
            flash('Session UID or Free Fire UID is required to stop spam', 'error')
            return redirect(url_for('index'))

        try:
            # Make request to stop the spam service using target UID
            stop_url = f"{SPAM_BASE_URL}/stop?id={target_uid}"
            response = requests.get(stop_url, timeout=10)

            if response.status_code == 200:
                # Update active spams list
                if session_uid and session_uid in active_spams:
                    active_spams[session_uid]['status'] = 'stopped'
                    active_spams[session_uid]['stopped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Save data to file
                    save_data(active_spams)
                flash(f'Free Fire spam stopped successfully for UID: {target_uid}', 'success')
                logger.info(f"Free Fire spam stopped for target UID: {target_uid}")
            else:
                flash(f'Failed to stop Free Fire spam. Status: {response.status_code}', 'error')
                logger.error(f"Failed to stop Free Fire spam for target UID: {target_uid}, Status: {response.status_code}")

        except requests.RequestException as e:
            flash(f'Error connecting to spam service: {str(e)}', 'error')
            logger.error(f"Request error for target UID {target_uid}: {str(e)}")

        return redirect(url_for('index'))

    return render_template('spam_form.html', action='stop', title='Stop Free Fire Spam')

@app.route('/spam_list')
def spam_list():
    """Display list of all spam sessions"""
    return render_template('spam_list.html', spams=active_spams)

@app.route('/developer')
def developer_info():
    """Developer information page"""
    return render_template('developer.html')

@app.route('/backup', methods=['POST'])
def create_data_backup():
    """Create a backup of the data file"""
    backup_file = create_backup()
    if backup_file:
        flash(f'Backup created successfully: {backup_file}', 'success')
        logger.info(f"Manual backup created: {backup_file}")
    else:
        flash('Failed to create backup', 'error')
    return redirect(url_for('spam_list'))

@app.route('/data_stats')
def data_stats():
    """Show data statistics"""
    try:
        file_size = os.path.getsize(DATA_FILE) if os.path.exists(DATA_FILE) else 0
        file_modified = datetime.fromtimestamp(os.path.getmtime(DATA_FILE)).strftime('%Y-%m-%d %H:%M:%S') if os.path.exists(DATA_FILE) else 'N/A'

        stats = {
            'total_sessions': len(active_spams),
            'active_sessions': len([s for s in active_spams.values() if s['status'] == 'active']),
            'stopped_sessions': len([s for s in active_spams.values() if s['status'] == 'stopped']),
            'file_size_bytes': file_size,
            'file_size_kb': round(file_size / 1024, 2),
            'last_modified': file_modified,
            'data_file': DATA_FILE
        }

        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/spam_list')
def api_spam_list():
    """API endpoint to get list of all spam sessions"""
    return jsonify({
        'status': 'success',
        'spams': list(active_spams.values()),
        'total': len(active_spams)
    })

@app.route('/clear_stopped', methods=['POST'])
def clear_stopped():
    """Clear all stopped spam sessions from the list"""
    global active_spams
    stopped_count = len([spam for spam in active_spams.values() if spam['status'] == 'stopped'])
    active_spams = {uid: spam for uid, spam in active_spams.items() if spam['status'] == 'active'}
    # Save data to file
    save_data(active_spams)
    flash(f'{stopped_count} stopped spam sessions cleared successfully', 'success')
    logger.info(f"Cleared {stopped_count} stopped sessions")
    return redirect(url_for('spam_list'))

@app.route('/delete_session/<session_id>', methods=['POST'])
def delete_session(session_id):
    """Delete a specific spam session from the list"""
    global active_spams
    if session_id in active_spams:
        spam_info = active_spams[session_id]
        del active_spams[session_id]
        # Save data to file
        save_data(active_spams)
        flash(f'Session deleted successfully: {session_id} (Free Fire UID: {spam_info.get("target_uid", "N/A")})', 'success')
        logger.info(f"Session deleted: {session_id}")
    else:
        flash(f'Session not found: {session_id}', 'error')
        logger.warning(f"Attempted to delete non-existent session: {session_id}")

    return redirect(url_for('spam_list'))

@app.route('/clear_all', methods=['POST'])
def clear_all():
    """Clear all spam sessions from the list"""
    global active_spams
    session_count = len(active_spams)
    active_spams.clear()
    # Save data to file
    save_data(active_spams)
    flash(f'All {session_count} spam sessions cleared successfully', 'success')
    logger.info(f"All {session_count} sessions cleared")
    return redirect(url_for('spam_list'))

@app.route('/api/spam_vip/<target_uid>')
def api_spam_vip(target_uid):
    """API endpoint for Free Fire spam VIP"""
    # Validate Free Fire UID
    if not is_valid_freefire_uid(target_uid):
        return jsonify({
            'status': 'error',
            'target_uid': target_uid,
            'message': 'Invalid Free Fire UID format. Must be 9-12 digits.'
        }), 400

    # Format the UID
    formatted_uid = format_freefire_uid(target_uid)

    # Generate session ID
    session_id = f"ff_api_{uuid.uuid4().hex[:8]}"

    try:
        spam_url = f"{SPAM_BASE_URL}/spam_vip?id={formatted_uid}"
        response = requests.get(spam_url, timeout=10)

        if response.status_code == 200:
            # Add to active spams list
            active_spams[session_id] = {
                'session_uid': session_id,
                'target_uid': formatted_uid,
                'status': 'active',
                'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'Free Fire VIP',
                'game': 'Free Fire'
            }
            # Save data to file
            save_data(active_spams)
            logger.info(f"API: Free Fire spam VIP started for target UID: {formatted_uid}, session: {session_id}")

        return jsonify({
            'status': 'success' if response.status_code == 200 else 'error',
            'session_id': session_id,
            'target_uid': formatted_uid,
            'message': f'Free Fire spam VIP {"started" if response.status_code == 200 else "failed"}',
            'service_response_code': response.status_code
        })
    except requests.RequestException as e:
        logger.error(f"API: Request error for target UID {formatted_uid}: {str(e)}")
        return jsonify({
            'status': 'error',
            'target_uid': formatted_uid,
            'message': f'Error connecting to spam service: {str(e)}'
        }), 500

@app.route('/api/stop/<identifier>')
def api_stop(identifier):
    """API endpoint for stopping Free Fire spam - accepts session_id or target_uid"""
    target_uid = None
    session_id = None

    # Check if identifier is a session ID in our active spams
    if identifier in active_spams:
        session_id = identifier
        target_uid = active_spams[identifier]['target_uid']
    else:
        # Treat as Free Fire UID
        if is_valid_freefire_uid(identifier):
            target_uid = format_freefire_uid(identifier)
            # Find session by target UID
            for sid, spam in active_spams.items():
                if spam.get('target_uid') == target_uid:
                    session_id = sid
                    break
        else:
            return jsonify({
                'status': 'error',
                'identifier': identifier,
                'message': 'Invalid identifier. Must be a valid session ID or Free Fire UID (9-12 digits).'
            }), 400

    if not target_uid:
        return jsonify({
            'status': 'error',
            'identifier': identifier,
            'message': 'Session not found or invalid Free Fire UID.'
        }), 404

    try:
        stop_url = f"{SPAM_BASE_URL}/stop?id={target_uid}"
        response = requests.get(stop_url, timeout=10)

        if response.status_code == 200 and session_id and session_id in active_spams:
            # Update active spams list
            active_spams[session_id]['status'] = 'stopped'
            active_spams[session_id]['stopped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Save data to file
            save_data(active_spams)
            logger.info(f"API: Free Fire spam stopped for target UID: {target_uid}, session: {session_id}")

        return jsonify({
            'status': 'success' if response.status_code == 200 else 'error',
            'session_id': session_id,
            'target_uid': target_uid,
            'identifier': identifier,
            'message': f'Free Fire spam {"stopped" if response.status_code == 200 else "stop failed"}',
            'service_response_code': response.status_code
        })
    except requests.RequestException as e:
        logger.error(f"API: Request error for target UID {target_uid}: {str(e)}")
        return jsonify({
            'status': 'error',
            'identifier': identifier,
            'target_uid': target_uid,
            'message': f'Error connecting to spam service: {str(e)}'
        }), 500

@app.route('/api/session/<session_id>')
def api_get_session(session_id):
    """API endpoint to get details of a specific session"""
    if session_id not in active_spams:
        return jsonify({
            'status': 'error',
            'session_id': session_id,
            'message': 'Session not found'
        }), 404

    return jsonify({
        'status': 'success',
        'session': active_spams[session_id]
    })

@app.route('/api/sessions/target/<target_uid>')
def api_get_sessions_by_target(target_uid):
    """API endpoint to get all sessions for a specific Free Fire UID"""
    if not is_valid_freefire_uid(target_uid):
        return jsonify({
            'status': 'error',
            'target_uid': target_uid,
            'message': 'Invalid Free Fire UID format'
        }), 400

    formatted_uid = format_freefire_uid(target_uid)
    matching_sessions = {
        sid: spam for sid, spam in active_spams.items()
        if spam.get('target_uid') == formatted_uid
    }

    return jsonify({
        'status': 'success',
        'target_uid': formatted_uid,
        'sessions': list(matching_sessions.values()),
        'count': len(matching_sessions)
    })

@app.route('/api/delete/<session_id>', methods=['DELETE'])
def api_delete_session(session_id):
    """API endpoint to delete a specific session"""
    if session_id not in active_spams:
        return jsonify({
            'status': 'error',
            'session_id': session_id,
            'message': 'Session not found'
        }), 404

    spam_info = active_spams[session_id]
    del active_spams[session_id]
    # Save data to file
    save_data(active_spams)
    logger.info(f"API: Session deleted: {session_id}")

    return jsonify({
        'status': 'success',
        'session_id': session_id,
        'deleted_session': spam_info,
        'message': 'Session deleted successfully'
    })

if __name__ == '__main__':
    # Get port from environment variable for Railway deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)