package main // glavnuy paket main tochka vhoda v programmu

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
)

// Sozdaem model polzovatelya
type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
}

// users-baza dannuyh v pamyati
var users = []User{
	{ID: 1, Username: "Alise", Email: "alice@example.com"},
	{ID: 2, Username: "Ferdinant", Email: "Ferdinant1@example.com"},
}

// main-tochka vhoda
func main() {
	// Obrabotchik dlya GET
	http.HandleFunc("/users", getUsers)

	// Obrabotchik dlya post // sozdaet novogo polzovatelya
	http.HandleFunc("/users/create", createUser)

	fmt.Println("Server is running on :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
func main() {
	// Obrabotchik dlya post // sozdaet novogo polzovatelya
	http.HandleFunc("/users/create", createUser)
	// Zapuskaem server na portu 8080
	log.Println("Server zapushen na http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func getUsers(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(users)
}

func createUser(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Метод не поддерживается", http.StatusMethodNotAllowed)
		return
	}

	// peremennaya kuda budem dekodirovat json
	var newuser User
	err := json.NewDecoder(r.Body).Decode(&newuser)
	if err != nil {
		http.Error(w, "Неверный json", http.StatusBadRequest)
		return
	}

	// Validaciya (proverim chto polya ne pustuye)
	if strings.TrimSpace(newuser.Username) == "" {
		http.Error(w, "Username pustoy", http.StatusBadRequest)
		return
	}

    // Dobavlyaem v nash spisok
    newuser.ID = len(users) + 1
    users = append(users, newuser)

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(newuser)
}
