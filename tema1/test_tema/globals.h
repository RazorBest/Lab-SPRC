#ifndef __GLOBALS_H__
#define __GLOBALS_H__

#include <unordered_set>
#include <unordered_map>
#include <queue>

struct file_permission {
    std::string path;
    int perm_flags;

    file_permission(std::string &path, int perm_flags)
        : path(path), perm_flags(perm_flags) {}
};

struct token_data {
    std::vector<file_permission> perms;
    int life;
};

class Globals {
public:
    std::unordered_set<std::string> users;
    std::queue<std::string> approve_queue;
    std::unordered_set<std::string> resource_db;
    std::unordered_map<std::string, token_data> token_db;
    std::unordered_map<std::string, std::string> regen_db;
    int token_ttl = 0;

    void init_server(
        const char *uid_file,
        const char *res_file,
        const char *approvals_file,
        const char *token_ttl_file);

private:
    void read_users(FILE *fin);
    void read_resources(FILE *fin);
    void read_approvals(FILE *fin);
    void read_token_ttl(FILE *fin);
};

extern Globals globals;

#endif //__GLOBALS_H__
