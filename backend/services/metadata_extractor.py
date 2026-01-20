import ast
import re
from typing import Dict, List, Optional, Tuple

def extract_python_metadata(file_content: str) -> Dict:
    """
    Extract imports, exports, and patterns from Python code
    """
    metadata = {
        "imports": [],
        "exports": [],
        "contains_api_routes": False,
        "contains_db_models": False,
        "contains_auth": False,
        "complexity_score": 0
    }
    
    try:
        tree = ast.parse(file_content)
        
        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    metadata["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    metadata["imports"].append(f"{module}.{alias.name}")
            
            # Extract class and function definitions
            elif isinstance(node, ast.ClassDef):
                metadata["exports"].append({
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno
                })
                
                # Check if it's a DB model
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        if base.id in ["Model", "BaseModel", "models.Model"]:
                            metadata["contains_db_models"] = True
            
            elif isinstance(node, ast.FunctionDef):
                metadata["exports"].append({
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno
                })
                
                # ✅ FIXED: Check for API route decorators
                for decorator in node.decorator_list:
                    # Handle decorator calls like @router.post('/path')
                    if isinstance(decorator, ast.Call):
                        # The func is what's being called (e.g., router.post)
                        if isinstance(decorator.func, ast.Attribute):
                            if decorator.func.attr in ["get", "post", "put", "delete", "patch", "route"]:
                                metadata["contains_api_routes"] = True
                        elif isinstance(decorator.func, ast.Name):
                            if decorator.func.id in ["get", "post", "put", "delete", "patch", "route"]:
                                metadata["contains_api_routes"] = True
                    
                    # Handle simple decorators like @route (without parentheses)
                    elif isinstance(decorator, ast.Attribute):
                        if decorator.attr in ["get", "post", "put", "delete", "patch", "route"]:
                            metadata["contains_api_routes"] = True
                    elif isinstance(decorator, ast.Name):
                        if decorator.id in ["get", "post", "put", "delete", "patch", "route"]:
                            metadata["contains_api_routes"] = True
        
        # Check for auth keywords
        auth_keywords = ["authenticate", "authorize", "jwt", "token", "login", "password", "hash"]
        content_lower = file_content.lower()
        metadata["contains_auth"] = any(keyword in content_lower for keyword in auth_keywords)
        
        # Calculate cyclomatic complexity (simplified)
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            # Count decision points
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        metadata["complexity_score"] = complexity
        
    except SyntaxError:
        # If file can't be parsed, return empty metadata
        pass
    
    return metadata

def extract_javascript_metadata(file_content: str) -> Dict:
    """
    Extract metadata from JavaScript/TypeScript files using regex
    (For production, use a proper parser like esprima)
    """
    metadata = {
        "imports": [],
        "exports": [],
        "contains_api_routes": False,
        "contains_db_models": False,
        "contains_auth": False,
        "complexity_score": 0
    }
    
    # Extract imports (ES6 style)
    import_patterns = [
        r'import\s+.*?\s+from\s+["\'](.+?)["\']',
        r'require\(["\'](.+?)["\']\)'
    ]
    for pattern in import_patterns:
        imports = re.findall(pattern, file_content)
        metadata["imports"].extend(imports)
    
    # Extract exports
    export_patterns = [
        r'export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)',
        r'module\.exports\s*=\s*(\w+)'
    ]
    for pattern in export_patterns:
        exports = re.findall(pattern, file_content)
        metadata["exports"].extend([{"type": "export", "name": e} for e in exports])
    
    # Check for API routes
    route_patterns = [
        r'app\.(get|post|put|delete|patch)\(',
        r'router\.(get|post|put|delete|patch)\(',
        r'@(Get|Post|Put|Delete|Patch)\('
    ]
    for pattern in route_patterns:
        if re.search(pattern, file_content):
            metadata["contains_api_routes"] = True
            break
    
    # Check for DB models
    model_patterns = [
        r'new\s+Schema\(',
        r'model\(',
        r'@Entity\(',
        r'sequelize\.define\('
    ]
    for pattern in model_patterns:
        if re.search(pattern, file_content):
            metadata["contains_db_models"] = True
            break
    
    # Check for auth
    auth_keywords = ["authenticate", "authorize", "jwt", "token", "login", "password"]
    content_lower = file_content.lower()
    metadata["contains_auth"] = any(keyword in content_lower for keyword in auth_keywords)
    
    # Calculate complexity (count if/while/for/switch)
    complexity = 1
    complexity += len(re.findall(r'\bif\s*\(', file_content))
    complexity += len(re.findall(r'\bwhile\s*\(', file_content))
    complexity += len(re.findall(r'\bfor\s*\(', file_content))
    complexity += len(re.findall(r'\bswitch\s*\(', file_content))
    metadata["complexity_score"] = complexity
    
    return metadata


def extract_metadata_by_extension(file_content: str, extension: str) -> Dict:
    """
    Route to the appropriate extractor based on file extension
    """
    if extension == ".py":
        return extract_python_metadata(file_content)
    elif extension in [".js", ".ts", ".tsx", ".jsx"]:
        return extract_javascript_metadata(file_content)
    else:
        # Default empty metadata for unsupported languages
        return {
            "imports": [],
            "exports": [],
            "contains_api_routes": False,
            "contains_db_models": False,
            "contains_auth": False,
            "complexity_score": 0
        }
