from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.config import settings

store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

class AgentService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sos un asistente virtual inteligente multicanal. Respondes de forma clara y concisa."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = self.prompt | self.llm

        self.agent_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def process_message(self, user_id: str, channel: str, message: str) -> str:
        session_id = f"{channel}_{user_id}"
        response = self.agent_with_history.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return response.content

agent_service = AgentService()