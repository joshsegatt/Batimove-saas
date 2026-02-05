"""
Email Service using Resend
Handles all email sending for Batimove
"""

import os
import resend
from typing import Dict, Any

# Initialize Resend with API key from environment
resend.api_key = os.environ.get("RESEND_API_KEY", "")

# Email configuration
COMPANY_EMAIL = "info@batimove.ch"
FROM_EMAIL = "Batimove Website <noreply@onboarding.resend.dev>"  # Temporary - change to noreply@batimove.ch when domain is configured


def send_quote_email(quote_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send quote request email to company
    
    Args:
        quote_data: Dictionary containing quote information
        
    Returns:
        Resend API response
    """
    
    # Extract contact info
    contact = quote_data.get('contact', {})
    service_id = quote_data.get('serviceId', 'N/A')
    
    # Map service IDs to French names
    service_names = {
        'priv': 'Déménagement Privé',
        'pro': 'Transfert Pro',
        'clean': 'Nettoyage',
        'storage': 'Garde-Meubles',
        'lift': 'Monte-Meubles',
        'inter': 'International',
        'general': 'Sur Mesure'
    }
    
    service_name = service_names.get(service_id, service_id)
    
    # Build HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #0052A3 0%, #003d7a 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #0052A3; }}
            .info-row {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #0052A3; display: inline-block; width: 150px; }}
            .value {{ color: #333; }}
            .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #666; font-size: 12px; }}
            .badge {{ background: #E10600; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚚 Nouvelle Demande de Devis</h1>
                <div class="badge">{service_name}</div>
            </div>
            
            <div class="content">
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #0052A3;">📋 Informations Client</h3>
                    <div class="info-row">
                        <span class="label">Nom:</span>
                        <span class="value">{contact.get('name', 'N/A')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Email:</span>
                        <span class="value"><a href="mailto:{contact.get('email', '')}">{contact.get('email', 'N/A')}</a></span>
                    </div>
                    <div class="info-row">
                        <span class="label">Téléphone:</span>
                        <span class="value"><a href="tel:{contact.get('phone', '')}">{contact.get('phone', 'N/A')}</a></span>
                    </div>
                </div>
                
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #0052A3;">📦 Détails du Service</h3>
                    <div class="info-row">
                        <span class="label">Service:</span>
                        <span class="value">{service_name}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Date souhaitée:</span>
                        <span class="value">{quote_data.get('date', 'N/A')}</span>
                    </div>
    """
    
    # Add service-specific details
    if quote_data.get('fromZip'):
        html_content += f"""
                    <div class="info-row">
                        <span class="label">NPA Départ:</span>
                        <span class="value">{quote_data.get('fromZip')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">NPA Arrivée:</span>
                        <span class="value">{quote_data.get('toZip', 'N/A')}</span>
                    </div>
        """
    
    if quote_data.get('volume'):
        html_content += f"""
                    <div class="info-row">
                        <span class="label">Volume:</span>
                        <span class="value">{quote_data.get('volume')} m³</span>
                    </div>
        """
    
    if quote_data.get('rooms'):
        html_content += f"""
                    <div class="info-row">
                        <span class="label">Nombre de pièces:</span>
                        <span class="value">{quote_data.get('rooms')}</span>
                    </div>
        """
    
    if quote_data.get('surface'):
        html_content += f"""
                    <div class="info-row">
                        <span class="label">Surface:</span>
                        <span class="value">{quote_data.get('surface')} m²</span>
                    </div>
        """
    
    if quote_data.get('housingType'):
        html_content += f"""
                    <div class="info-row">
                        <span class="label">Type de bien:</span>
                        <span class="value">{quote_data.get('housingType').capitalize()}</span>
                    </div>
        """
    
    html_content += """
                </div>
                
                <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
                    <p style="margin: 0; font-size: 14px; color: #0052A3;">
                        <strong>⏰ Action requise:</strong> Contactez ce client sous 24h pour établir un devis personnalisé.
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>Batimove Sarl | Rue de Monthoux 64, 1201 Genève</p>
                <p>Ce message a été généré automatiquement depuis le site web.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    try:
        params = {
            "from": FROM_EMAIL,
            "to": [COMPANY_EMAIL],
            "subject": f"🚚 Nouveau Devis: {service_name} - {contact.get('name', 'Client')}",
            "html": html_content
        }
        
        response = resend.Emails.send(params)
        return {"success": True, "id": response.get("id")}
    
    except Exception as e:
        print(f"Error sending quote email: {str(e)}")
        raise


def send_contact_email(contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send contact form message to company
    
    Args:
        contact_data: Dictionary containing contact form data
        
    Returns:
        Resend API response
    """
    
    name = contact_data.get('name', 'N/A')
    email = contact_data.get('email', 'N/A')
    subject = contact_data.get('subject', 'Question Générale')
    message = contact_data.get('message', '')
    
    # Build HTML email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #0052A3 0%, #003d7a 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #0052A3; }}
            .info-row {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #0052A3; display: inline-block; width: 100px; }}
            .value {{ color: #333; }}
            .message-box {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border: 2px solid #e3f2fd; }}
            .footer {{ text-align: center; margin-top: 20px; padding: 20px; color: #666; font-size: 12px; }}
            .badge {{ background: #E10600; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💬 Nouveau Message de Contact</h1>
                <div class="badge">{subject}</div>
            </div>
            
            <div class="content">
                <div class="info-box">
                    <h3 style="margin-top: 0; color: #0052A3;">👤 Informations de Contact</h3>
                    <div class="info-row">
                        <span class="label">Nom:</span>
                        <span class="value">{name}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Email:</span>
                        <span class="value"><a href="mailto:{email}">{email}</a></span>
                    </div>
                    <div class="info-row">
                        <span class="label">Sujet:</span>
                        <span class="value">{subject}</span>
                    </div>
                </div>
                
                <div class="message-box">
                    <h3 style="margin-top: 0; color: #0052A3;">📝 Message</h3>
                    <p style="white-space: pre-wrap; margin: 0;">{message}</p>
                </div>
                
                <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
                    <p style="margin: 0; font-size: 14px; color: #0052A3;">
                        <strong>⏰ Action requise:</strong> Répondez à ce message sous 24h.
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>Batimove Sarl | Rue de Monthoux 64, 1201 Genève</p>
                <p>Ce message a été généré automatiquement depuis le formulaire de contact.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    try:
        params = {
            "from": FROM_EMAIL,
            "to": [COMPANY_EMAIL],
            "subject": f"💬 Contact: {subject} - {name}",
            "html": html_content,
            "reply_to": email  # Allow direct reply to customer
        }
        
        response = resend.Emails.send(params)
        return {"success": True, "id": response.get("id")}
    
    except Exception as e:
        print(f"Error sending contact email: {str(e)}")
        raise
