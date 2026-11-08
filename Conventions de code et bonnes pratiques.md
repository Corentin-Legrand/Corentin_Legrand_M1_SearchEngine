## I. Principes généraux

Un code propre est **lisible, simple et cohérent**.  
Il doit être **facile à comprendre, maintenir et faire évoluer**.

**Objectifs :**
- Clarté avant tout.
- Pas de redondance (principe **DRY**).
- Cohérence du style et du vocabulaire.
- Code explicite plutôt que commenté.

---

## II. Nommage

### Règles générales
- **Tout le code est en anglais.**
- Les noms doivent être **explicites et cohérents**.
- Pas d’abréviations ou de préfixes inutiles.

### Méthodes et fonctions
- Nom sous forme **verbe + complément** :
  - Procédure (modifie un état) → `doSomething()`
  - Fonction (retourne une valeur) → `getSomething()`

```csharp
public User GetUserById(int id)
public Exercise CreateExercise(Exercise exercise)
```

### Collections et booléens
```csharp
private List<User> users; // ✅ pluriel
bool isActive; bool hasErrors; bool canExecute; // is - has - can
```

### Exceptions et tests
- Exceptions : les fichiers et classes se terminent par `Exception`
  - *En Python*, la convention est de terminer par `Error` (ex. `UserNotFoundError`), comme les exceptions natives (`ValueError`, `KeyError`…).
- Tests : les fichiers et classes se terminent par `Test` 
exemple -> fichier : `NomDeClasseTests.cs` / classe : `NomDeClasseTests`
  - *En Python*, fichiers `test_*.py` (pytest) ou classes `Test...` (unittest).

---

### Conventions par langage

#### TypeScript
| Élément                              | Convention                  |
| ------------------------------------ | --------------------------- |
| Variables / Fonctions                | `camelCase`                 |
| Constantes                           | `UPPER_SNAKE_CASE`          |
| Classes / Interfaces / Types / Enums | `PascalCase` *(pas de “I”)* |
| Fichiers                             | `kebab-case`                |

#### C sharp#
| Élément            | Convention          |
| ------------------ | ------------------- |
| Variables          | `camelCase`         |
| Méthodes / Classes | `PascalCase`        |
| Interfaces         | `I` + `PascalCase`  |
| Fichiers           | `PascalCase`        |

```csharp
public interface IUser {}
```

#### Python *(PEP 8)*
| Élément                                        | Convention                          |
| ---------------------------------------------- | ----------------------------------- |
| Variables / Fonctions / Méthodes / Attributs   | `snake_case`                        |
| Constantes                                     | `UPPER_SNAKE_CASE`                  |
| Classes / Exceptions / Enums                   | `PascalCase` *(pas de “I”)*         |
| Interfaces *(classe abstraite)*                | `I` + `PascalCase` (ex. `IUserService`) |
| Membres d’énumération                          | `UPPER_SNAKE_CASE`                  |
| Fichiers / Modules / Packages                  | `snake_case`                        |
| Attribut « protégé » / « privé »               | `_name` / `__name` *(name mangling)* |

- Python n’a pas d’interfaces natives : on les implémente avec une **classe de base abstraite** (`ABC` + `@abstractmethod`), **préfixée par `I`** (voir §VI).
- Le préfixe `_` exprime une intention « non public » ; le préfixe `__` déclenche le *name mangling* (voir §VI).

```python
class User:
    ...

MAX_RETRY_COUNT = 10
```

---

## III. Typage

- **Toujours typer** attributs, paramètres, variables et retours.  
- *En Python*, le typage se fait via les **annotations de type (type hints)**. Elles sont **indicatives** (non vérifiées à l’exécution) mais restent **obligatoires** dans notre convention ; elles sont exploitées par les outils d’analyse statique (**mypy**, **pyright**, **Pylance**).

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)

age: int = 30
```

---

## IV. Documentation et commentaires

- Documentation **en anglais** pour tout (pas le privé).  
- Mentionner **l’auteur** dans la doc des classes.
- Mentionner **l’auteur** dans les méthodes modifiées (sinon par défaut on supposera que l'auteur d'une méthode = auteur de la classe)
- Commenter **seulement si nécessaire** (ex. regex ou logique complexe).  
- Si le code a besoin d’un commentaire, il doit souvent être simplifié.

##### Exemple en C sharp
``` C#
/// <summary>
/// Represents a user.
/// </summary>
/// <remarks>
/// Author: John Doe
/// </remarks>
public class User
{
}

/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="id">The user's identifier.</param>
/// <returns>The <see cref="User"/> instance matching the given ID.</returns>
/// <exception cref="UserNotFoundException">
/// Thrown when no user exists with the specified ID.
/// </exception>
/// <remarks>
/// Author: Jane Smith
/// </remarks>
public static User GetUserById(int id)
{
    if (id <= 0)
        throw new UserNotFoundException($"User with ID {id} not found.");

    return someone;
}
```
##### Exemple en TS
``` TS
/**
 * Represents a user in the system.
 * @author John Doe
 */
export class User {}

/**
 * Retrieves a user by their unique identifier.
 * @param {number} id - The user's identifier.
 * @returns {User} The user instance matching the given ID.
 * @throws {UserNotFoundError} If no user exists with the specified ID.
 * @author Jane Smith
 */
static getUserById(id: number): User {
  if (id <= 0) {
    throw new UserNotFoundError(`User with ID ${id} not found.`);
  }
  return someone;
}
```

##### Documentation en Python (docstring)

**Nomenclature (style Google adapté) :**
- Docstring **en anglais**, entourée de triples guillemets doubles `"""..."""`, placée **juste après** la déclaration (module, classe, fonction/méthode).
- **Ligne 1** : résumé court, à l’impératif/présent, terminé par un point.
- Puis, si utile : une ligne vide, une description plus détaillée, et les sections dans l’ordre : `Args:`, `Returns:`, `Raises:`, `Attributes:` (pour les classes).
- **Indiquer le type dans la docstring**, entre parenthèses pour les paramètres et attributs, en préfixe pour le retour :
  - Paramètre → `user_id (int): description`
  - Attribut → `name (str): description`
  - Retour → `Returns:` puis `<Type>: description` (ex. `User: ...`)
  - Exception → `Raises:` puis `<Exception>: condition`
- **Auteur** : ajouter une ligne `Author: Prénom Nom` en fin de docstring des **classes** (et des **méthodes modifiées**, sinon l’auteur par défaut = auteur de la classe).

```python
class User:
    """Represents a user in the system.

    Attributes:
        name (str): The user's display name.
        email (str): The user's email address.

    Author: John Doe
    """

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


def get_user_by_id(user_id: int) -> User:
    """Retrieve a user by their unique identifier.

    Args:
        user_id (int): The user's identifier.

    Returns:
        User: The user instance matching the given ID.

    Raises:
        UserNotFoundError: If no user exists with the specified ID.

    Author: Jane Smith
    """
    if user_id <= 0:
        raise UserNotFoundError(f"User with ID {user_id} not found.")

    return someone
```

> **Rappel :** le type est **explicitement indiqué dans la docstring** (`Args`, `Returns`, `Raises`, `Attributes`). Les paramètres et le retour des fonctions conservent en plus leurs *annotations* dans la signature (§III) ; les **propriétés / attributs** ne sont **pas** annotés au niveau de la classe — leur type est porté par la section `Attributes:`.

---

## V. Structure et style

### Organisation
- Classe ≤ **200 lignes** de code logique (hors documentation), méthode ≤ **30 lignes**.
- Méthodes avec peu d’arguments, faible imbrication (< 3 niveaux).
- Supprimer le **code mort**.
- **Initialiser** les variables à la déclaration.

### Style
```csharp
if (a)
{
    b;
}
```
- Une seule instruction `return` par méthode.
- Éviter les indirections multiples :  
  `var tmp = a.b; tmp.c = 3;`
- Ne pas comparer des flottants avec `==`.

> *En Python* : indentation **4 espaces** (jamais de tabulations), respect de **PEP 8**. Point d’entrée protégé par `if __name__ == "__main__":`. Privilégier les **f-strings** pour l’affichage. Jamais d’objet **mutable** comme valeur par défaut d’un argument (`def f(x, acc=[])` → utiliser `acc=None`).

---

## VI. Conception orientée objet

### Fonctions vs procédures
- **Fonction** → obtient un état.  
- **Procédure** → modifie un état.

### Objets vs structures
| Objet                       | Structure (DTO ou struct)  |
| --------------------------- | -------------------------- |
| Fournit un **comportement** | Contient des **données**   |
| Cache son implémentation    | Peut exposer ses attributs |
| Attributs privés            | Attributs publics tolérés  |
| Pas d’accesseurs directs    | Propriétés possibles       |

> *En Python*, une structure de données simple peut être un **`@dataclass`** (génère `__init__`, `__repr__`, `__eq__`).

### Encapsulation
- Les objets **ne révèlent pas leur implémentation**.
- Les attributs sont **privés**.
- Les propriétés publiques sont **limitées**.

> *En Python* :
> - Attribut « privé » via le préfixe `__` (*name mangling*) ; « protégé » via `_`. Rien n’est réellement privé : la convention exprime une **intention**.
> - Pour un accès contrôlé, utiliser la forme **pythonique `@property`** / `@x.setter` (validation dans le setter) **plutôt que** des accesseurs `get_x()` / `set_x()`.

```python
class Account:
    """A bank account.

    Attributes:
        balance (float): The current balance; never negative.

    Author: John Doe
    """

    def __init__(self, balance: float = 0) -> None:
        self.__balance = balance

    @property
    def balance(self):
        """Return the current balance.

        Returns:
            float: The current balance.
        """
        return self.__balance

    @balance.setter
    def balance(self, value):
        """Set the balance after validation.

        Args:
            value (float): The new balance.

        Raises:
            ValueError: If the balance is negative.
        """
        if value < 0:
            raise ValueError("Negative balance is not allowed.")
        self.__balance = value
```

### Interfaces
Les interfaces restent **obligatoires** dès que le bon respect de la POO l’exige (abstraction, découplage, inversion de dépendances). Python n’ayant pas de mot-clé `interface`, on les définit avec une **classe de base abstraite** :

- Hériter de **`ABC`** et marquer **chaque** méthode du contrat avec **`@abstractmethod`** (corps `...`, aucune implémentation).
- **Nommer** l’interface avec le préfixe **`I`** + `PascalCase` (ex. `IUserService`).
- **Indiquer explicitement dans la docstring** qu’il s’agit d’une interface (en plus du préfixe `I`).
- Une classe concrète **implémente** l’interface en en héritant et en fournissant **toutes** les méthodes abstraites (sinon elle ne peut pas être instanciée).

```python
from abc import ABC, abstractmethod


class IUserService(ABC):
    """Interface for the user service.

    Author: John Doe
    """

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """Retrieve a user by their unique identifier.

        Args:
            user_id (int): The user's identifier.

        Returns:
            User: The user instance matching the given ID.

        Raises:
            UserNotFoundError: If no user exists with the specified ID.
        """
        ...


class UserService(IUserService):
    """Concrete implementation of the user service.

    Author: John Doe
    """

    def get_user_by_id(self, user_id: int) -> User:
        if user_id <= 0:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return someone
```

---

## VII. Gestion des erreurs

- Le code d’erreur doit être **isolé** du métier.  
- Ne pas retourner `null` : préférer **exceptions** ou **valeurs par défaut**.
- Les `try/catch` doivent être **courts et clairs**, idéalement dans la **couche IHM**.
- Ne pas utiliser les exceptions comme flux logique.

> *En Python* : `try` / `except` / `else` / `finally` ; **lever** avec `raise`. Ne pas retourner `None` pour signaler une erreur → préférer une exception dédiée (suffixe `Error`). Capturer des exceptions **précises** (jamais `except:` nu).

---

## VIII. Tests

### Règles FIRST
| Principe            | Signification       |
| ------------------- | ------------------- |
| **Fast**            | Rapide              |
| **Independent**     | Indépendant         |
| **Repeatable**      | Reproductible       |
| **Self-validating** | Résultat binaire    |
| **Timely**          | Écrit avant le code |

### Bonnes pratiques
- Un test = une vérification.
- Noms descriptifs et explicites.
- Tests automatisés, reproductibles, sans dépendances.

> *En Python* : **pytest** (ou `unittest`). Fichiers `test_*.py`, fonctions `test_...`, une assertion logique par test.

---

## IX. Constantes et valeurs magiques

- Ne pas utiliser de **valeurs “magiques”**.  
- Utiliser des **constantes** ou **énumérations**.

```csharp
public class Example
{
    public const int MaxRetryCount = 10;
}
```

> *En Python* : constantes en `UPPER_SNAKE_CASE` au niveau du module, ou **`Enum`** pour un ensemble de valeurs.

```python
from enum import Enum

MAX_RETRY_COUNT = 10


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
```

---

## ✅ Résumé rapide

| Thème | Règle clé |
|--------|------------|
| **Lisibilité** | Code clair et cohérent |
| **Nommage** | En anglais, explicite |
| **Typage** | Toujours explicite |
| **Structure** | Petites classes et méthodes |
| **Erreurs** | Isolées, jamais silencieuses |
| **Objets** | Cachent leur implémentation |
| **Tests** | FIRST : Fast, Independent, Repeatable, Self-validating, Timely |
