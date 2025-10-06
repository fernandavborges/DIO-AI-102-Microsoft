from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analyse_credit_card(card_url):
    try:
        credential = AzureKeyCredential(Config.SUBSCRIPTION_KEY)

        documentClient = DocumentIntelligenceClient(Config.ENDPOINT, credential)

        cardInfo = documentClient.begin_analyze_document("prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url))

        result = cardInfo.result()

        for document in result.documents:
            fields = document.get('fields', {})

            return {
                "card_name": fields.get('CardHolderName', {}).get('content'),
                "card_number": fields.get('CardNumber', {}).get('content'),
                "expiry_date": fields.get('ExpirationDate', {}).get('content'),
                "bank_name": fields.get('IssuingBank', {}).get('content'),
            }
    except Exception as ex:
        return None