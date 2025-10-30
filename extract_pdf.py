#!/usr/bin/env python3
import pdfplumber
import json
import re

def extract_pdf_content(pdf_path):
    """Extrae contenido del PDF y lo estructura"""
    content = {
        'text': '',
        'pages': [],
        'images': [],
        'company_info': {},
        'services': [],
        'contact_info': {}
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Procesando PDF con {len(pdf.pages)} páginas...")
            
            for i, page in enumerate(pdf.pages):
                print(f"Procesando página {i+1}...")
                page_text = page.extract_text()
                if page_text:
                    content['pages'].append({
                        'page_number': i + 1,
                        'text': page_text
                    })
                    content['text'] += page_text + "\n\n"
                
                # Extraer imágenes
                if hasattr(page, 'images') and page.images:
                    for img in page.images:
                        if 'bbox' in img:
                            content['images'].append({
                                'page': i + 1,
                                'bbox': img['bbox'],
                                'width': img.get('width', 0),
                                'height': img.get('height', 0)
                            })
            
            # Extraer información específica de la empresa
            content['company_info'] = extract_company_info(content['text'])
            content['services'] = extract_services(content['text'])
            content['contact_info'] = extract_contact_info(content['text'])
            
    except Exception as e:
        print(f"Error al procesar PDF: {e}")
    
    return content

def extract_company_info(text):
    """Extrae información de la empresa"""
    info = {}
    
    # Buscar nombre de la empresa
    company_patterns = [
        r'TEKON\s+REDLINE',
        r'Tekon\s+Redline',
        r'tekon\s+redline'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info['name'] = match.group().strip()
            break
    
    # Buscar RUT
    rut_pattern = r'RUT:\s*(\d{1,2}\.\d{3}\.\d{3}-[\dkK])'
    rut_match = re.search(rut_pattern, text, re.IGNORECASE)
    if rut_match:
        info['rut'] = rut_match.group(1)
    
    # Buscar misión, visión, valores
    mission_pattern = r'(?:MISIÓN|Mision)[:\s]*(.+?)(?:\n|$)'
    mission_match = re.search(mission_pattern, text, re.IGNORECASE | re.DOTALL)
    if mission_match:
        info['mission'] = mission_match.group(1).strip()
    
    vision_pattern = r'(?:VISIÓN|Vision)[:\s]*(.+?)(?:\n|$)'
    vision_match = re.search(vision_pattern, text, re.IGNORECASE | re.DOTALL)
    if vision_match:
        info['vision'] = vision_match.group(1).strip()
    
    return info

def extract_services(text):
    """Extrae servicios de la empresa"""
    services = []
    
    # Patrones para buscar servicios
    service_patterns = [
        r'(?:Servicios?|SERVICIOS?)[:\s]*(.+?)(?:\n\n|\n[A-Z]|$)',
        r'•\s*(.+?)(?:\n|$)',
        r'-\s*(.+?)(?:\n|$)',
        r'\d+\.\s*(.+?)(?:\n|$)'
    ]
    
    for pattern in service_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            if isinstance(match, str) and len(match.strip()) > 5:
                services.append(match.strip())
    
    return list(set(services))  # Eliminar duplicados

def extract_contact_info(text):
    """Extrae información de contacto"""
    contact = {}
    
    # Buscar teléfonos
    phone_patterns = [
        r'Tel[éf]?fono[:\s]*(\+?[\d\s\-\(\)]+)',
        r'Fono[:\s]*(\+?[\d\s\-\(\)]+)',
        r'(\+?56\s?\d{1,2}\s?\d{4}\s?\d{4})',
        r'(\+?56\s?\d{8,9})'
    ]
    
    phones = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        phones.extend(matches)
    
    if phones:
        contact['phones'] = list(set(phones))
    
    # Buscar emails
    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    emails = re.findall(email_pattern, text)
    if emails:
        contact['emails'] = list(set(emails))
    
    # Buscar dirección
    address_patterns = [
        r'Dirección[:\s]*(.+?)(?:\n|$)',
        r'Dirección[:\s]*(.+?)(?:\n[A-Z]|$)',
        r'Address[:\s]*(.+?)(?:\n|$)'
    ]
    
    for pattern in address_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            contact['address'] = match.group(1).strip()
            break
    
    return contact

if __name__ == "__main__":
    pdf_path = "02-BROCHURE-TKREDLINE 2025.pdf"
    content = extract_pdf_content(pdf_path)
    
    # Guardar en archivo JSON
    with open('extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print("Contenido extraído y guardado en 'extracted_content.json'")
    print(f"Páginas procesadas: {len(content['pages'])}")
    print(f"Servicios encontrados: {len(content['services'])}")
    print(f"Información de contacto: {content['contact_info']}")
