from models.project_info import ProjectInfo
from services.project_service import ProjectService

info = ProjectInfo()

info.name = "ForgeBud"

info.version = "0.3.0"

info.description = "AI Software Development Workspace"

info.language = "Python"

info.framework = "PySide6"

ProjectService.initialize(".", info)

loaded = ProjectService.load(".")

print(loaded)

print(ProjectService.is_initialized("."))