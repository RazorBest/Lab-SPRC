#include "./globals.h"

#include <cstring>


Globals globals;

void Globals::read_users(FILE *fin) {
    int n_users;
    char uid[128];

    fscanf(fin, "%d", &n_users);

    for (int i = 0; i < n_users; i++) {
        fscanf(fin, "%s", uid);
        if (strlen(uid) != 15) {
            printf("UID doesn't have length 15");
            exit(1);
        }

        this->users.insert(uid);
    }
}

// Reads the list of files from the resources 
// file and stores them in the variable resource_db
void Globals::read_resources(FILE *fin) {
    int n_resources;
    char file[128];

    fscanf(fin, "%d", &n_resources);

    for (int i = 0; i < n_resources; i++) {
        fscanf(fin, "%s", file);
        this->resource_db.insert(file);
    }
}

void Globals::read_approvals(FILE *fin) {
    char buf[256];

    while(fgets(buf, sizeof(buf), fin)) {
        int len = strlen(buf);
        
        if (buf[len - 1] == '\n') {
            buf[len - 1]  = '\0';
        }

        this->approve_queue.push(buf);
    }
}

void Globals::read_token_ttl(FILE *fin) {
    char buf[256];
    fscanf(fin, "%d", &(this->token_ttl));
}

void Globals::init_server(const char *uid_file, const char *res_file,
        const char *approvals_file, const char *token_ttl_file) {
    FILE *fin;

    // Read the users
    fin = fopen(uid_file, "r");
    if (fin == NULL) {
        perror("fopen");
        exit(1);
    }
    read_users(fin);
    fclose(fin);

    // Read the resources
    fin = fopen(res_file, "r");
    if (fin == NULL) {
        perror("fopen");
        exit(1);
    }
    read_resources(fin);
    fclose(fin);

    // Read the permissions
    fin = fopen(approvals_file, "r");
    if (fin == NULL) {
        perror("fopen");
        exit(1);
    }
    read_approvals(fin);
    fclose(fin);

    // Read the token ttl
    fin = fopen(token_ttl_file, "r");
    if (fin == NULL) {
        perror("fopen");
        exit(1);
    }
    read_token_ttl(fin);
    fclose(fin);
}
