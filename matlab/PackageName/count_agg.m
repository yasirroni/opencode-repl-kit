function result = count_agg(data, column)
    % count_agg - Count of non-null values in a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %
    % Returns:
    %   Count of non-null values.

    if isempty(data)
        result = 0;
        return;
    end

    values = extract_values(data, column);
    result = sum(~isnan(values));
end

function values = extract_values(data, column)
    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end
end
