// traverse a tree level by level
#include <iostream>
#include <queue>
#include <vector>
struct TreeNode
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

std::vector<std::vector<int>> levelOrder(TreeNode *root)
{
    std::vector<std::vector<int>> result;

    if (!root)
    {
        return result; // Return an empty vector for an empty tree.
    }

    std::queue<TreeNode *> q;
    q.push(root);

    while (!q.empty())
    {
        int levelSize = q.size();
        std::vector<int> currentLevel;

        for (int i = 0; i < levelSize; ++i)
        {
            TreeNode *node = q.front();
            q.pop();
            currentLevel.push_back(node->val);

            if (node->left)
            {
                q.push(node->left);
            }
            if (node->right)
            {
                q.push(node->right);
            }
        }

        result.push_back(currentLevel);
    }

    return result;
}

int main()
{
    // Example tree:
    //       1
    //      / \
    //     2   3
    //    / \
    //   4   5

    TreeNode *root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);

    std::vector<std::vector<int>> levels = levelOrder(root);

    // Print the levels
    for (const std::vector<int> &level : levels)
    {
        for (int val : level)
        {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
