import abc 
import os 

from pathlib import Path

from typing import Optional, NoReturn, List
from dataclasses import dataclass


@dataclass
class Component(metaclass=abc.ABCMeta):
    abstraction: Optional[float] = None
    inestability: Optional[float] = None 
    
    external_dependencies: float = 0.0 
    internal_dependencies: float = 0.0 
    
    no_abstract_classes: float = 0.0 
    abstract_classes: float = 0.0 
    
    def add_dependency(self, is_internal=False) -> NoReturn:
        if is_internal:
            self.internal_dependencies += 1 
        else: 
            self.external_dependencies += 1
    
    def add_class(self, is_abstract=True) -> NoReturn: 
        if is_abstract:
            self.abstract_classes += 1 
        else:
            self.no_abstract_classes += 1


class ComponentLoader(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def load_component(self, *args, **kwargs) -> Component:
        raise NotImplementedError()


@dataclass
class ModuleComponent(Component):
    module_name: str 
    path: str 


class ModuleComponentLoader(ComponentLoader):
    
    components = []
    
    def load_component(self, root_path: str) -> ModuleComponent:
        
        self.get_py_modules(root_path)
        
    
    def _find_py_modules(self, root, modules) -> List[Path]:
        py_modules = []
        for module in modules:
            if not module.endswith(".py"):
                continue
            
            module_path = os.path.join(root, module)
            py_modules.append(module_path)
    
        return py_modules

    def _find_py_packages(self, root, packages) -> List[Path]:
        py_packages = []
        for package in packages:
            package_path = os.path.join(root, package)
            
            if "__init__.py" not in os.listdir(package_path):
                continue 
            
            py_packages.append(package_path)
            
        return py_packages
    
    def get_py_modules(self, root_path: str):
        
        py_modules = []
        py_packages = [root_path]
        
        while not py_packages:
            py_package = py_packages.pop(0)
            for root, packages, modules in os.walk(py_package, topdown=True):
                
                py_modules.extend(self._find_py_modules(root, modules))
                py_packages.extend(self._find_py_packages(root, packages))

        return py_modules
